import argparse
import os
import sys
import textwrap

# function declaration template
function_declaration = '''    void %(name)s(HTTPServerRequest& req, HTTPServerResponse& resp, vector<string>& params);
'''

# function declaration template
function_definition = '''    // %(line)s
    void %(name)s(HTTPServerRequest& request, HTTPServerResponse& response, vector<string>& params)
    {
        response.setChunkedTransferEncoding(true);
        response.setContentType("application/json");
        std::ostream& ostr = response.send();
        ostr << R"x({ "request" : "%(line)s" })x";
    }

'''

# STL map entry template
mapEntry = '''    {{R"x(%(line)s)x"}, WebService::%(name)s},
'''


class Formatter(argparse.HelpFormatter):
    """Helper class for help formatting"""

    def _fill_text(self, text, width, indent):
        return ''.join(indent + line for line in text.splitlines(keepends=True))

    def _split_lines(self, text, width):
        return text.splitlines()

    def _get_help_string(self, action):
        h = action.help
        if '%(default)' not in action.help:
            if action.default is not argparse.SUPPRESS:
                defaulting_nargs = [argparse.OPTIONAL, argparse.ZERO_OR_MORE]
                if action.option_strings or action.nargs in defaulting_nargs:
                    h += ' (default: %(default)s)'
        return h


class WSGenerator:
    """Code generator to create a web server that handle predefined URIs"""

    def __init__(self, args):
        self.args = args
        # The following names correspond to names in the templates
        self.function_prototypes = ""
        self.functions = ""
        self.urlMap = ""

    def generate(self):
        with open(self.args.uris) as f:
            for index, line in enumerate(f):
                line = line.rstrip()
                line = line.replace("<param>", "([^/]+)")
                name = 'route{:03d}'.format(index)
                self.functions += function_definition % locals()
                self.function_prototypes += function_declaration % locals()
                self.urlMap += mapEntry % locals()
        self.functions = self.functions.rstrip()
        self.urlMap = self.urlMap.rstrip()[:-1]

        for name in os.listdir(self.args.templates):
            with open(self.args.templates + '/' + name) as f_in:
                content = f_in.read()
            dest = self.get_destination(name)
            with open(dest, 'w+') as f:
                print(content % self.__dict__, file=f)

    def get_destination(self, name):
        dest = (self.args.source_dest, self.args.header_dest)[name.endswith('.h')]
        try:
            os.makedirs(dest)
        except:
            pass
        return dest + '/' + name


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog=os.path.basename(sys.argv[0]),
        description=textwrap.dedent('''\
            Generate code for a simple web server that handles a given set of URIs.'''),
        epilog=textwrap.dedent('''\
        Example:
            %(prog)s --uris ./my_uris_file --templates my_template_dir
            '''),
        formatter_class=Formatter)
    parser.add_argument('--uris', type=str, default='examples/uris.txt',
                        help='file containing URIs for code generation')
    parser.add_argument('--templates', type=str, default='templates',
                        help='directory containing templates')
    parser.add_argument('--source_dest', type=str, default='src',
                        help='directory where source files will be generated')
    parser.add_argument('--header_dest', type=str, default='include',
                        help='directory where header files will be generated')
    cli_args = parser.parse_args()

    WSGenerator(cli_args).generate()
