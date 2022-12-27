package com.bangkit.yourney.domain.model

import android.os.Parcelable
import kotlinx.parcelize.Parcelize

@Parcelize
data class Favorite (
    val liked: Boolean? = false,
    val message: String? = null
) : Parcelable