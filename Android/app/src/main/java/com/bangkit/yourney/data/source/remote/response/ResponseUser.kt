package com.bangkit.yourney.data.source.remote.response

import kotlinx.parcelize.Parcelize
import android.os.Parcelable
import com.google.gson.annotations.SerializedName

@Parcelize
data class ResponseUser(

	@field:SerializedName("user")
	val user: UserData? = null,

	@field:SerializedName("status")
	val status: String? = null
) : Parcelable