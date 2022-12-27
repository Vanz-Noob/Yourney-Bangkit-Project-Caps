package com.bangkit.yourney.domain.model

import android.os.Parcelable
import com.google.gson.annotations.SerializedName
import kotlinx.parcelize.Parcelize

@Parcelize
data class Destination (
    val namaDesinasi: String? = null,
    val namaDestinasi: String? = null,
    val idDestinasi: Int? = null,
    val urlDestinasi: String? = null,
    val picDestinasi: String? = null,
    val deskripsi: String? = null,
    val idKategoriDestinasi: Int? = null
) : Parcelable