package com.bangkit.yourney.data.sharedpreference

import android.content.Context
import android.content.SharedPreferences
import com.bangkit.yourney.domain.model.User
import com.bangkit.yourney.utils.Constanta.SHARED_PREFS_LOGIN
import com.bangkit.yourney.utils.Constanta.SHARED_PREFS_USER
import com.google.gson.Gson

class AuthPreference(context: Context) {
    private var preference: SharedPreferences

    init {
        preference = context.getSharedPreferences(SHARED_PREFS_LOGIN, Context.MODE_PRIVATE)
    }

    val authData: User?
        get() = Gson().fromJson(
            preference.getString(SHARED_PREFS_USER, null),
            User::class.java
        ) ?: null

    val getToken: String
        get() = "Bearer ${Gson().fromJson(
            preference.getString(SHARED_PREFS_USER, null),
            User::class.java
        ).access}"

    fun saveAuthData(account: User?) {
        val editor = preference.edit()
        val accData = Gson().toJson(account)
        editor.putString(SHARED_PREFS_USER, accData)
        editor.apply()
    }
}