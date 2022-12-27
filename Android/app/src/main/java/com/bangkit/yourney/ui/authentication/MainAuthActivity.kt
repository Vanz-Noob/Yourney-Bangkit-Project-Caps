package com.bangkit.yourney.ui.authentication

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import com.bangkit.yourney.databinding.ActivityLoginBinding
import com.bangkit.yourney.databinding.ActivityMainAuthBinding
import com.jaeger.library.StatusBarUtil

class MainAuthActivity : AppCompatActivity() {
    private lateinit var binding: ActivityMainAuthBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainAuthBinding.inflate(layoutInflater)
        setContentView(binding.root)

        with(binding) {
            btnMasuk.setOnClickListener {
                Intent(this@MainAuthActivity, LoginActivity::class.java).apply {
                    startActivity(this)
                }
            }
            btnRegister.setOnClickListener {
                Intent(this@MainAuthActivity, RegisterActivity::class.java).apply {
                    startActivity(this)
                }
            }
        }
    }
}