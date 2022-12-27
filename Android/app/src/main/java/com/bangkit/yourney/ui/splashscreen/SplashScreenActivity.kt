package com.bangkit.yourney.ui.splashscreen

import android.annotation.SuppressLint
import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.view.WindowManager
import com.bangkit.yourney.data.sharedpreference.AuthPreference
import com.bangkit.yourney.data.sharedpreference.IntroPreference
import kotlinx.coroutines.*
import com.bangkit.yourney.databinding.ActivitySplashScreenBinding
import com.bangkit.yourney.ui.authentication.MainAuthActivity
import com.bangkit.yourney.ui.intro.IntroActivity
import com.bangkit.yourney.ui.main.HomeActivity

@SuppressLint("CustomSplashScreen")
class SplashScreenActivity : AppCompatActivity() {
    private lateinit var binding: ActivitySplashScreenBinding

    @OptIn(DelicateCoroutinesApi::class)
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivitySplashScreenBinding.inflate(layoutInflater)
        setContentView(binding.root)

        window.setFlags(
            WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON,
            WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON
        )

        GlobalScope.launch {
            delay(3000)
            withContext(Dispatchers.Main) {
//                Intent(this@SplashScreenActivity, HomeActivity::class.java).apply {
//                    startActivity(this)
//                }
                if(IntroPreference(this@SplashScreenActivity).isFirstime) {
                    IntroPreference(this@SplashScreenActivity).saveStatus(false)
                    Intent(this@SplashScreenActivity, IntroActivity::class.java).apply {
                        startActivity(this)
                    }
                } else {
                    val loginData = AuthPreference(this@SplashScreenActivity).authData
                    if(loginData?.access != null)
                        Intent(this@SplashScreenActivity, HomeActivity::class.java).apply {
                            startActivity(this)
                        }
                    else
                        Intent(this@SplashScreenActivity, MainAuthActivity::class.java).apply {
                            startActivity(this)
                        }
                }
                finish()
            }
        }
    }
}