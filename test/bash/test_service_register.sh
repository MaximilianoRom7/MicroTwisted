# Invalid Service Registration 1
curl_post '{' http://0.0.0.0:5000/service/register; echo
# Invalid Service Registration 2
curl_post '{}' http://0.0.0.0:5000/service/register; echo
# Valid Service Registrations 3
curl_post '{"service-hash": "123", "service-url": "http://"}' http://0.0.0.0:5000/service/register; echo
curl_post '{"service-hash": "123", "service-url": "http://www.google.com"}' http://0.0.0.0:5000/service/register; echo
curl_post '{"service-hash": "123", "service-url": "http://www.facebook.com"}' http://0.0.0.0:5000/service/register; echo
