require "http/client"
require "json"

if ARGV.size < 1
    puts "Usage: findmac <mac-address>"
    exit
end

macaddress = ARGV[0]

url = "https://api.macvendors.com/#{macaddress}"

response = HTTP::Client.get(url)
content_type = response.headers["Content-Type"]? || ""

if content_type.includes?("application/json")
    begin
        body = JSON.parse(response.body)
        if body["errors"]? && body["errors"]["detail"]?.try(&.as_s) == "Not Found"
        puts "No vendor found."
        end
    rescue ex : JSON::ParseException
        puts "API response was invalid: #{ex.message}"
    rescue ex
        puts "Failed to make a request: #{ex.message}"
    end
else
    puts response.body
end