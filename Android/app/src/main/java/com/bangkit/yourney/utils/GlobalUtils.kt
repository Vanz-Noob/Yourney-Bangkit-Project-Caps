package com.bangkit.yourney.utils

import android.content.Context
import android.widget.Toast
import com.bangkit.yourney.data.source.remote.response.ResponseDefault
import com.google.gson.Gson

object GlobalUtils {
    fun showToast(message: String, context: Context) {
        Toast.makeText(context, message, Toast.LENGTH_SHORT).show()
    }

    fun getErrorMessageFromJSON(text: String) : String {
        return Gson().fromJson(text, ResponseDefault::class.java).message!!
    }
}