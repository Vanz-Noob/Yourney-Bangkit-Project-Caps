package com.bangkit.yourney.data.source.remote.response

import com.google.gson.annotations.SerializedName
import kotlinx.parcelize.Parcelize
import android.os.Parcelable

@Parcelize
data class ResponseDefault (

    @field:SerializedName("message")
    val message: String? = null

) : Parcelable
