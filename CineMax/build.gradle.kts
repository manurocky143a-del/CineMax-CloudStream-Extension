// use an integer for version numbers
version = 1

cloudstream {
    language = "ta"
    // All of these properties are optional, you can safely remove them

    description = "An independent CloudStream extension for CineMax"
    authors = listOf("CineMax Devs")

    /**
     * Status int as the following:
     * 0: Down
     * 1: Ok
     * 2: Slow
     * 3: Beta only
     * */
    status = 1 // will be 3 if unspecified
    tvTypes = listOf(
        "Movie",
        "TvSeries"
    )

    iconUrl = ""
}
