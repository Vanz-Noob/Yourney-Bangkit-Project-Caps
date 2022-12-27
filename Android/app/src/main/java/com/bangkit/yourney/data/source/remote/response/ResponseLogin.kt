package com.bangkit.yourney.data.source.remote.response

import kotlinx.parcelize.Parcelize
import android.os.Parcelable
import com.google.gson.annotations.SerializedName

@Parcelize
data class ResponseLogin(

	@field:SerializedName("access")
	val access: String? = null,

	@field:SerializedName("refresh")
	val refresh: String? = null,

	@field:SerializedName("user")
	val user: UserData? = null,

	@field:SerializedName("status")
	val status: String? = null,

	@field:SerializedName("message")
	val message: String? = null
) : Parcelable