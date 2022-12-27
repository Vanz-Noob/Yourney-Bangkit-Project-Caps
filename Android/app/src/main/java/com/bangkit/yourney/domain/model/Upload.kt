package com.bangkit.yourney.domain.model

import kotlinx.parcelize.Parcelize
import android.os.Parcelable
import com.google.gson.annotations.SerializedName

@Parcelize
data class Upload(
	val url: String? = null,
	val message: String? = null,
	val status: String? = null
) : Parcelable