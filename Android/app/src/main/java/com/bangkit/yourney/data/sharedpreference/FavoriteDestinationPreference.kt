package com.bangkit.yourney.data.sharedpreference

import android.content.Context
import android.content.SharedPreferences
import com.bangkit.yourney.domain.model.Destination
import com.bangkit.yourney.domain.model.User
import com.bangkit.yourney.utils.Constanta.SHARED_PREFS_FAVORITE
import com.bangkit.yourney.utils.Constanta.SHARED_PREFS_USER
import com.google.gson.Gson
import com.google.gson.reflect.TypeToken
import java.lang.reflect.Type


class FavoriteDestinationPreference(context: Context) {
    private var preference: SharedPreferences

    init {
        preference = context.getSharedPreferences(SHARED_PREFS_FAVORITE, Context.MODE_PRIVATE)
    }

    fun listFavoriteDestination(): List<Destination>? {
        val json = preference.getString(SHARED_PREFS_FAVORITE, null)
        val type: Type = object : TypeToken<List<Destination?>?>() {}.type
        return Gson().fromJson(json, type)
    }


    fun saveFavorite(data: List<Destination>) {
        val editor = preference.edit()
        val accData = Gson().toJson(data)
        editor.putString(SHARED_PREFS_FAVORITE, accData)
        editor.apply()
    }
}