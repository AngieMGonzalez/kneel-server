import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from views import (
    get_all_metals,
    get_single_metal,
    create_metal,
    delete_metal,
    update_metal,
    get_all_styles,
    get_single_style,
    create_style,
    delete_style,
    update_style,
    get_all_orders,
    get_single_order,
    create_order,
    delete_order,
    update_order,
    get_all_sizes,
    get_single_size,
    create_size,
    delete_size,
    update_size
)

class HandleRequests(BaseHTTPRequestHandler):
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server
    """
    # the instance of itself is self = languages that use instances
    # instatiation is creating an instance
    def parse_url(self, path):
        """
        This method splits the client path string into parts to isolate the requested id. 
        """
        # dot notate on method
        # you can [] notate on a dictionary
        # Just like splitting a string in JavaScript. If the
        # path is "/animals/1", the resulting list will
        # have "" at index 0, "animals" at index 1, and "1"
        # at index 2.
        path_params = path.split("/")
        resource = path_params[1]
        id = None

        # Try to get the item at index 2
        try:
            # Convert the string "1" to the integer 1
            # This is the new parseInt()
            id = int(path_params[2])
        except IndexError:
            pass  # No route parameter exists: /animals
        except ValueError:
            pass  # Request had trailing slash: /animals/

        return (resource, id)  # This is a tuple

    def do_GET(self):
        """GET all/single resource/s requests server
        """
        self._set_headers(200)
        response = {}
        # Parse the URL and capture the tuple that is returned
        (resource, id) = self.parse_url(self.path)

        if resource == "metals":
            if id is not None:
                response = get_single_metal(id)
                # response = { "message": f"Metal {id} is rocking out" }
            else:
                response = get_all_metals()
        elif resource == "orders":
            if id is not None:
                response = get_single_order(id)
            else:
                response = get_all_orders()
        elif resource == "sizes":
            if id is not None:
                response = get_single_size(id)
            else:
                response = get_all_sizes()
        elif resource == "styles":
            if id is not None:
                response = get_single_style(id)
            else:
                response = get_all_styles()

        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        """Handles POST aka CREATE requests to the server
        """
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        # Convert JSON string to a Python dictionary
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)
        # id is defining how you split the URL, its aLIST and u do need the id
        # you could do like self.path[0]

        # Initialize new resource
        if resource == "orders":
            new_order = create_order(post_body)
            # Encode the new resource and send in response
            self.wfile.write(json.dumps(new_order).encode())

        if resource == "metals":
            new_metal = create_metal(post_body)
            self.wfile.write(json.dumps(new_metal).encode())

        if resource == "sizes":
            new_size = create_size(post_body)
            self.wfile.write(json.dumps(new_size).encode())

        if resource == "styles":
            new_style = create_style(post_body)
            self.wfile.write(json.dumps(new_style).encode())

    def do_PUT(self):
        """PUT update_entry server request replace WHOLE resource
        """
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        success = False

        # Update a single resource in the list
        if resource == "orders":
            update_order(id, post_body)
        elif resource == "metals":
            update_metal(id, post_body)
        elif resource == "sizes":
            update_size(id, post_body)
        elif resource == "styles":
            update_style(id, post_body)

        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)

        # Encode the order and send in response
        self.wfile.write("".encode())

    def do_DELETE(self):
        """deletes resource
        """
        # sets a 204 response code
        self._set_headers(204)

        # parse the URL
        (resource, id) = self.parse_url(self.path)

        if resource == "metals":
            delete_metal(id)
        if resource == "orders":
            delete_order(id)
        if resource == "sizes":
            delete_size(id)
        if resource == "styles":
            delete_style(id)

        self.wfile.write("".encode())

    def _set_headers(self, status):
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        """Sets the options headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                        'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                        'X-Requested-With, Content-Type, Accept')
        self.end_headers()


# point of this application.
def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
