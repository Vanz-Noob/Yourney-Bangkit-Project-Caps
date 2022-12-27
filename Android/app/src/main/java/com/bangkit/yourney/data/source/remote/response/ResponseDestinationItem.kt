package com.bangkit.yourney.data.source.remote.response

import kotlinx.parcelize.Parcelize
import android.os.Parcelable
import com.google.gson.annotations.SerializedName

@Parcelize
data class ResponseDestinationItem(

	@field:SerializedName("nama_destinasi")
	val namaDestinasi: String? = null,

	@field:SerializedName("nama_desinasi")
	val namaDesinasi: String? = null,

	@field:SerializedName("id_destinasi")
	val idDestinasi: Int? = null,

	@field:SerializedName("url_destinasi")
	val urlDestinasi: String? = null,

	@field:SerializedName("pic_destinasi")
	val picDestinasi: String? = null,

	@field:SerializedName("deskripsi")
	val deskripsi: String? = null,

	@field:SerializedName("id_kategori_destinasi")
	val idKategoriDestinasi: Int? = null
) : Parcelable