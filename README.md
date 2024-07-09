# Mock Data 
* 91 unique locations
* 1823 unique hotels
    * With exception handling, you may get double the number of hotels. 
    * This happened to me in two cases that I just re-ran manually.
    * Total time (with cleaning) was 12 minutes.  Total gen time was around 5 minutes.
    * Cost with the 70b model was $0.38
* 7292 room rates (4 different room types per hotel)
    * Sourcing required about 30 minutes.
    * 1 exception occurred when the AST parsed correctly, but missed the database format.
    * The script hung when Replicate didn't return on one answer.
    * Everything else completed correctly (upon further inspection) in about 30 minutes.
    * Cost with the 70b model was $2.00
    * 1792 unique room types
* Hotel image space
    * travelectable.db prior to image loading = 2465792 bytes