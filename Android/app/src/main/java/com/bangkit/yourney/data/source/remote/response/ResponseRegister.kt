package com.bangkit.yourney.data.source.remote.response

import kotlinx.parcelize.Parcelize
import android.os.Parcelable
import com.google.gson.annotations.SerializedName

@Parcelize
data class ResponseRegister(

	@field:SerializedName("code")
	val code: String? = null,

	@field:SerializedName("tempat_lahir")
	val tempatLahir: String? = null,

	@field:SerializedName("jenis_kelamin")
	val jenisKelamin: String? = null,

	@field:SerializedName("username")
	val username: String? = null,

	@field:SerializedName("message")
	val message: String? = null

) : Parcelable