package com.bangkit.yourney.domain.model

import android.os.Parcelable
import com.google.gson.annotations.SerializedName
import kotlinx.parcelize.Parcelize

@Parcelize
data class User (

    val user_id: Int? = null,
    val avatar: String? = null,
    val status: String? = null,
    val username: String? = null,
    val full_name: String? = null,
    var email: String? = null,
    val password: String? = null,
    val tempatLahir: String? = null,
    val jenisKelamin: String? = null,
    val username_twitter: String? = null,
    var access: String? = null,
    var refresh: String? = null,
    var message: String? = null

) : Parcelable