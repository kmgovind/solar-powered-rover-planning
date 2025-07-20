using HTTP, CSV, DataFrames, Dates, Plots

# Function to load environment variables from a file
function load_env_file(filename::String)
    for line in eachline(filename)
        if isempty(strip(line)) || startswith(strip(line), "#")
            continue
        end
        k, v = split(line, "=", limit=2)
        ENV[strip(k)] = strip(v)
    end
end

# Load your API key
load_env_file("secrets.env")

# Fetch CSV data from NREL NSRDB API for Ann Arbor, MI (30-min interval)
resp = HTTP.get(
    "https://developer.nrel.gov/api/nsrdb/v2/solar/nsrdb-GOES-aggregated-v4-0-0-download.csv";
    query = [
        "api_key"    => ENV["NREL_API_KEY"],
        "email"      => ENV["MY_EMAIL"],
        "wkt"        => "POINT(-83.7430 42.2808)",  # Ann Arbor
        "names"      => "2022",
        "attributes" => "ghi,dni,dhi",
        "interval"   => "30",
        "utc"        => "true",
        "leap_day"   => "false",
    ]
)

# Save the raw response to a CSV file
output_file = "nrel_data.csv"
write(output_file, resp.body)
println("Data saved to $output_file")

# # Parse the CSV response
# df = CSV.read(IOBuffer(resp.body), DataFrame; header=false)

# # Debug: Check the number of columns
# println("Number of columns in DataFrame: ", size(df, 2))

# # Select only the first 8 columns if the response contains extra columns
# if size(df, 2) > 8
#     println("Trimming DataFrame to the first 8 columns")
#     df = select(df, 1:8)
# end

# # Define column names
# column_names = [:Year, :Month, :Day, :Hour, :Minute, :GHI, :DNI, :DHI]

# # Rename columns
# rename!(df, column_names)

# # Build timestamp from date/time components
# df.Timestamp = DateTime.(
#     string.(df.Year, "-", df.Month, "-", df.Day, " ",
#             df.Hour, ":", df.Minute),
#     dateformat"y-m-d H:M"
# )

# # Plot GHI vs. time
# plot(
#     df.Timestamp,
#     df.GHI,
#     xlabel = "Time",
#     ylabel = "GHI (W/m²)",
#     title = "Global Horizontal Irradiance in Ann Arbor (2022)",
#     legend = false,
#     lw = 0.8,
#     color = :orange
# )
