#ifndef WEBSERVICE_H
#define WEBSERVICE_H

#include "Poco/Net/HTTPRequestHandler.h"
#include "Poco/Net/HTTPRequestHandlerFactory.h"
#include "Poco/Net/HTTPServer.h"
#include "Poco/Net/HTTPServerParams.h"
#include "Poco/Net/HTTPServerRequest.h"
#include "Poco/Net/HTTPServerResponse.h"
#include "Poco/Net/ServerSocket.h"

#include <csignal>
#include <cstdlib>
#include <functional>
#include <iostream>
#include <memory>
#include <regex>
#include <string>
#include <unordered_map>
#include <vector>

using namespace Poco::Net;
using namespace std;

#include "WebServiceFunctions.h"
#endif
