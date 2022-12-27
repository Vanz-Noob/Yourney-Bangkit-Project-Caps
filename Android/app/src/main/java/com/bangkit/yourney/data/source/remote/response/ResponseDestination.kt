package com.bangkit.yourney.data.source.remote.response

import kotlinx.parcelize.Parcelize
import android.os.Parcelable
import com.google.gson.annotations.SerializedName

@Parcelize
data class ResponseDestination(
	@field:SerializedName("")
	val responseDestination: List<ResponseDestinationItem?>? = null
) : Parcelable