package com.bangkit.yourney.utils

import android.widget.ImageView
import com.bangkit.yourney.data.sharedpreference.AuthPreference
import com.bumptech.glide.load.DataSource
import com.bumptech.glide.load.engine.GlideException
import com.bumptech.glide.load.resource.gif.GifDrawable
import com.bumptech.glide.request.RequestListener
import com.bumptech.glide.request.target.Target
import com.jakewharton.picasso.OkHttp3Downloader
import com.squareup.picasso.Picasso
import okhttp3.Interceptor
import okhttp3.OkHttpClient
import okhttp3.Request


object ImageViewUtils {
    fun ImageView.loadImageFromLocal(id: Int?) {
        GlideApp.with(this.context)
            .load(id)
            .into(this)
    }

    fun ImageView.loadImageFromServerWithAuth(url: String) {
        val client: OkHttpClient = OkHttpClient.Builder()
            .addInterceptor(Interceptor { chain ->
                val newRequest = chain.request().newBuilder()
                    .addHeader("Authorization", AuthPreference(this.context).getToken)
                    .build()
                chain.proceed(newRequest)
            })
            .build()

        Picasso.Builder(context)
            .downloader(OkHttp3Downloader(client))
            .build()
            .load(url)
            .into(this)

//        picasso.load(url).into(this)
    }

    fun ImageView.loadImageFromServer(url: String?) {
        GlideApp.with(this.context)
            .load("$url")
            .into(this)
    }

    fun ImageView.loadGIFDrawable(id: Int, loop: Boolean) {
        GlideApp.with(this.context)
            .asGif()
            .load(id)
            .listener(object : RequestListener<GifDrawable> {
                override fun onResourceReady(
                    resource: GifDrawable?,
                    model: Any?,
                    target: Target<GifDrawable>?,
                    dataSource: DataSource?,
                    isFirstResource: Boolean
                ): Boolean {
                    if(!loop) resource?.setLoopCount(1)
                    return false
                }

                override fun onLoadFailed(
                    e: GlideException?,
                    model: Any?,
                    target: Target<GifDrawable>?,
                    isFirstResource: Boolean
                ): Boolean {
                    return false
                }
            })
            .into(this)
    }
}