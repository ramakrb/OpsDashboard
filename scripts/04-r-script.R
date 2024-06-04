

library(httr)
library(fs)

print("Checking which files we have:")
dir_ls()

#  the URL 
url_download = "https://www.usbr.gov/lc/region/g4000/NaturalFlow/LFnatFlow1906-2024.2024.4.22.xlsx"

# file name to save
file_name = paste0("LFnatFlow1906-2024_", Sys.Date(), ".xlsx")


print("Making a POST request and writing file on disk:")
POST(url_download, write_disk(file_name, overwrite = TRUE))


print("Checking which files we have:")
dir_ls()
