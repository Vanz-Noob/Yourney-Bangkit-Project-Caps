package com.bangkit.yourney.data.sharedpreference

import android.content.Context
import android.content.SharedPreferences
import com.bangkit.yourney.domain.model.User
import com.bangkit.yourney.utils.Constanta.SHARED_PREFS_INTRO
import com.bangkit.yourney.utils.Constanta.SHARED_PREFS_LOGIN
import com.bangkit.yourney.utils.Constanta.SHARED_PREFS_TUTOR
import com.bangkit.yourney.utils.Constanta.SHARED_PREFS_USER
import com.google.gson.Gson

class IntroPreference(context: Context) {
    private var preference: SharedPreferences

    init {
        preference = context.getSharedPreferences(SHARED_PREFS_INTRO, Context.MODE_PRIVATE)
    }

    val isFirstime: Boolean
        get() = preference.getBoolean(SHARED_PREFS_INTRO, true)

    fun saveStatus(status: Boolean) {
        val editor = preference.edit()
        editor.putBoolean(SHARED_PREFS_INTRO, status)
        editor.apply()
    }

    val isFirstimeTutorial: Boolean
        get() = preference.getBoolean(SHARED_PREFS_TUTOR, true)

    fun saveStatusTutor(status: Boolean) {
        val editor = preference.edit()
        editor.putBoolean(SHARED_PREFS_TUTOR, status)
        editor.apply()
    }
}