package com.bangkit.yourney.domain.model

import android.os.Parcelable
import kotlinx.parcelize.Parcelize

@Parcelize
data class Slider (
    val title: String? = null,
    val subtitle: String? = null,
    val image: Int? = null,
) : Parcelable