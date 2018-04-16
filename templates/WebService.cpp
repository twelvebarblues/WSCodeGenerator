#include "WebService.h"
#include "WebServiceFunctions.h"

struct Key
{
    Key(string s) : rx(s), key(s)
    {
    }
    bool operator==(const Key& k) const
    {
        return key == k.key;
    }
    regex rx;
    string key;
};

struct Hash
{
    size_t operator()(const Key& k) const
    {
        return hash<string>()(k.key);
    }
};

unordered_map<Key, function<void(HTTPServerRequest&, HTTPServerResponse&, vector<string>&)>, Hash> urlMap = {
    %(urlMap)s
};

struct RequestHandler : public HTTPRequestHandler
{
    void handleRequest(HTTPServerRequest& request, HTTPServerResponse& response)
    {
        for (auto& k : urlMap)
        {
            string url = request.getMethod() + request.getURI();
            smatch matches;
            if (regex_match(url, matches, k.first.rx))
            {
                vector<string> params;
                for (unsigned int i = 1; i < matches.size(); ++i)
                {
                    string m = matches[i];
                    params.push_back(m);
                }
                k.second(request, response, params);
                return;
            }
        }
        response.setStatus(HTTPResponse::HTTPStatus::HTTP_NOT_FOUND);
        response.setContentType("application/json");
        std::ostream& ostr = response.send();
        ostr << R"x(
        {
            "action": "Not Found",
            "code": "404",
            "customCode": "0",
            "description": "Not Found",
            "summary": "Not Found"
        })x";
    }
};

struct RequestHandlerFactory : public HTTPRequestHandlerFactory
{
    HTTPRequestHandler* createRequestHandler(const HTTPServerRequest& request)
    {
        return new RequestHandler();
    }
};

class WebServer
{
  public:
    WebServer(unsigned int port = 9980) : port_(port)
    {
    }

    int run()
    {
        ServerSocket svs(port_);
        HTTPServer srv(new RequestHandlerFactory, svs, new HTTPServerParams);
        srv.start();
        wait();
        srv.stop();
        return EXIT_SUCCESS;
    }

  private:
    void wait()
    {
        sigset_t sset;
        sigemptyset(&sset);
        sigaddset(&sset, SIGQUIT);
        sigaddset(&sset, SIGTERM);
        sigprocmask(SIG_BLOCK, &sset, NULL);
        int sig;
        sigwait(&sset, &sig);
    }
    unsigned int port_ = 9980;
};

int main(int argc, char** argv)
{
    WebServer app;
    return app.run();
}
