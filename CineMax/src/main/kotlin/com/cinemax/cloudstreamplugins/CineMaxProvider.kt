package com.cinemax.cloudstreamplugins

import com.cinemax.cloudstreamplugins.entities.EpisodesData
import com.cinemax.cloudstreamplugins.entities.MiniModalInfo
import com.cinemax.cloudstreamplugins.entities.PlayList
import com.cinemax.cloudstreamplugins.entities.PostData
import com.cinemax.cloudstreamplugins.entities.SearchData
import com.lagradost.cloudstream3.*
import com.lagradost.cloudstream3.utils.*
import com.lagradost.cloudstream3.utils.AppUtils.toJson
import com.lagradost.cloudstream3.utils.AppUtils.tryParseJson
import com.lagradost.cloudstream3.utils.ExtractorLink
import com.lagradost.cloudstream3.utils.Qualities
import com.lagradost.cloudstream3.utils.httpsify
import com.lagradost.cloudstream3.utils.getQualityFromName
import okhttp3.Headers
import okhttp3.Interceptor
import okhttp3.Response
import org.jsoup.nodes.Element
import com.lagradost.cloudstream3.APIHolder.unixTime

class CineMaxProvider : MainAPI() {
    override val supportedTypes = setOf(
        TvType.Movie,
        TvType.TvSeries,
    )
    override var lang = "en"

    override var mainUrl = "https://net77.cc"
    override var name = "CineMax"

    override val hasMainPage = true
    private val headers = mapOf(
        "X-Requested-With" to "XMLHttpRequest"
    )

    override suspend fun getMainPage(page: Int, request: MainPageRequest): HomePageResponse? {
        val categories = listOf(
            "Trending Movies" to "movie",
            "Popular Action" to "action",
            "Comedy" to "comedy",
            "Popular Drama" to "drama"
        )
        val homePageLists = categories.mapNotNull { (categoryName, query) ->
            val url = "$mainUrl/search.php?s=$query&t=${APIHolder.unixTime}"
            try {
                val data = app.get(url, referer = "$mainUrl/", headers = headers).parsed<SearchData>()
                val items = data.searchResult.filter { it.id.isNotEmpty() }.map { res ->
                    val title = if (res.t.isNotEmpty()) res.t else "Title ${res.id}"
                    newAnimeSearchResponse(title, Id(res.id).toJson()) {
                        this.posterUrl = "https://img.nfmirrorcdn.top/poster/v/${res.id}.jpg"
                        posterHeaders = mapOf("Referer" to "$mainUrl/")
                    }
                }
                if (items.isNotEmpty()) HomePageList(categoryName, items) else null
            } catch (e: Exception) {
                e.printStackTrace()
                null
            }
        }

        return newHomePageResponse(homePageLists, false)
    }

    override suspend fun search(query: String): List<SearchResponse> {
        val url = "$mainUrl/search.php?s=$query&t=${APIHolder.unixTime}"
        val data = app.get(url, referer = "$mainUrl/", headers = headers).parsed<SearchData>()

        return data.searchResult.filter { it.id.isNotEmpty() }.map { res ->
            val title = if (res.t.isNotEmpty()) res.t else "Title ${res.id}"
            newAnimeSearchResponse(title, Id(res.id).toJson()) {
                posterUrl = "https://img.nfmirrorcdn.top/poster/v/${res.id}.jpg"
                posterHeaders = mapOf("Referer" to "$mainUrl/")
            }
        }
    }

    override suspend fun load(url: String): LoadResponse? {
        val id = parseJson<Id>(url).id

        // Fetch mini modal info for metadata (runtime, genre, rating)
        val miniModalUrl = "$mainUrl/mini-modal-info.php?id=$id&t=${APIHolder.unixTime}"
        val modalInfo = try {
            app.get(miniModalUrl, referer = "$mainUrl/", headers = headers).parsed<MiniModalInfo>()
        } catch (e: Exception) {
            null
        }

        // Fetch playlist to retrieve title
        val playlistUrl = "$mainUrl/playlist.php?id=$id&t=&tm=${APIHolder.unixTime}"
        val playlist = try {
            app.get(playlistUrl, referer = "$mainUrl/", headers = headers).parsed<PlayList>()
        } catch (e: Exception) {
            null
        }

        val title = playlist?.firstOrNull()?.title ?: "Title $id"
        val genres = modalInfo?.genre?.split(",")?.map { it.trim() }?.filter { it.isNotEmpty() } ?: emptyList()
        val tags = if (modalInfo?.ua != null) listOf(modalInfo.ua) + genres else genres
        val duration = convertRuntimeToMinutes(modalInfo?.runtime ?: "")

        val episodes = arrayListOf<Episode>()

        // Try episodes endpoint to see if it's a TV show with seasons/episodes
        val episodesUrl = "$mainUrl/episodes.php?s=$id&series=$id&t=${APIHolder.unixTime}"
        val episodesData = try {
            app.get(episodesUrl, referer = "$mainUrl/", headers = headers).parsed<EpisodesData>()
        } catch (e: Exception) {
            null
        }

        if (episodesData?.episodes.orEmpty().isNotEmpty()) {
            episodesData?.episodes?.filterNotNull()?.mapTo(episodes) { ep ->
                newEpisode(LoadData(title, ep.id)) {
                    this.name = ep.t
                    this.episode = ep.ep.replace("E", "").toIntOrNull()
                    this.season = ep.s.replace("S", "").toIntOrNull()
                    this.posterUrl = "https://img.nfmirrorcdn.top/epimg/150/${ep.id}.jpg"
                    this.runTime = ep.time.replace("m", "").toIntOrNull()
                }
            }
        } else {
            episodes.add(newEpisode(LoadData(title, id)) {
                this.name = title
            })
        }

        val isTvSeries = episodesData?.episodes.orEmpty().isNotEmpty() || modalInfo?.runtime?.contains("Season") == true

        return if (isTvSeries) {
            newTvSeriesLoadResponse(title, url, TvType.TvSeries, episodes) {
                this.posterUrl = "https://img.nfmirrorcdn.top/poster/v/$id.jpg"
                this.backgroundPosterUrl = "https://img.nfmirrorcdn.top/poster/h/$id.jpg"
                this.posterHeaders = mapOf("Referer" to "$mainUrl/")
                this.plot = "Watch $title on CineMax"
                this.tags = tags
                this.duration = duration
            }
        } else {
            newMovieLoadResponse(title, url, TvType.Movie, LoadData(title, id)) {
                this.posterUrl = "https://img.nfmirrorcdn.top/poster/v/$id.jpg"
                this.backgroundPosterUrl = "https://img.nfmirrorcdn.top/poster/h/$id.jpg"
                this.posterHeaders = mapOf("Referer" to "$mainUrl/")
                this.plot = "Watch $title on CineMax"
                this.tags = tags
                this.duration = duration
            }
        }
    }

    override suspend fun loadLinks(
        data: String,
        isCasting: Boolean,
        subtitleCallback: (SubtitleFile) -> Unit,
        callback: (ExtractorLink) -> Unit
    ): Boolean {
        val (title, id) = parseJson<LoadData>(data)
        val playlistUrl = "$mainUrl/playlist.php?id=$id&t=${title.replace(" ", "%20")}&tm=${APIHolder.unixTime}"
        val playlist = app.get(playlistUrl, referer = "$mainUrl/", headers = headers).parsed<PlayList>()

        playlist.forEach { item ->
            item.sources.forEach { source ->
                callback.invoke(
                    newExtractorLink(
                        name,
                        source.label,
                        fixUrl(source.file),
                        type = ExtractorLinkType.M3U8
                    ) {
                        this.referer = "$mainUrl/"
                        this.quality = getQualityFromName(source.file.substringAfter("q=", ""))
                    }
                )
            }

            item.tracks?.filter { it.kind == "captions" }?.map { track ->
                subtitleCallback.invoke(
                    SubtitleFile(
                        track.label.toString(),
                        fixUrl(track.file.toString())
                    )
                )
            }
        }

        return true
    }

    @Suppress("ObjectLiteralToLambda")
    override fun getVideoInterceptor(extractorLink: ExtractorLink): Interceptor? {
        return object : Interceptor {
            override fun intercept(chain: Interceptor.Chain): Response {
                val request = chain.request()
                if (request.url.toString().contains(".m3u8")) {
                    val newRequest = request.newBuilder()
                        .header("Cookie", "hd=on")
                        .build()
                    return chain.proceed(newRequest)
                }
                return chain.proceed(request)
            }
        }
    }

    data class Id(
        val id: String
    )

    data class LoadData(
        val title: String, val id: String
    )
}
