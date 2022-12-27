package com.bangkit.yourney.ui.authentication

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import android.view.View
import com.bangkit.yourney.R
import com.bangkit.yourney.data.Resource
import com.bangkit.yourney.data.sharedpreference.AuthPreference
import com.bangkit.yourney.databinding.ActivityLoginBinding
import com.bangkit.yourney.ui.main.HomeActivity
import com.bangkit.yourney.utils.DialogUtils
import com.bangkit.yourney.utils.GlobalUtils
import com.bangkit.yourney.utils.GlobalUtils.showToast
import org.koin.androidx.viewmodel.ext.android.viewModel

class LoginActivity : AppCompatActivity() {
    private lateinit var binding: ActivityLoginBinding
    private val viewModel: AuthViewModel by viewModel()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityLoginBinding.inflate(layoutInflater)
        setContentView(binding.root)

        with(binding) {
            btnMasuk.setOnClickListener {
                processLogin()
            }
            btnBack.setOnClickListener {
                finish()
            }
//            tvRegister.setOnClickListener {
//                Intent(this@LoginActivity, RegisterActivity::class.java).apply {
//                    startActivity(this)
//                }
//            }
        }
    }

    private fun processLogin() {
        with(binding) {
            when {
                tietUsername.text.toString().isEmpty() -> {
                    tilUsername.error = "Required"
                }
                tietPassword.text.toString().isEmpty() -> {
                    tilPassword.error = "Required"
                }
                else -> {
                    viewState(isLoading = true, showView = false)
                    tietUsername.error = null
                    tietPassword.error = null

                    val livedata = viewModel.authLogin(
                        tietUsername.text.toString(),
                        tietPassword.text.toString()
                    )
                    livedata.observe(this@LoginActivity) { data ->
                        if (data != null) {
                            when (data) {
                                is Resource.Loading<*> -> {
                                    Log.d("TAG_LOADING", "JUST LOADING")
                                }
                                is Resource.Success<*> -> {
                                    livedata.removeObservers(this@LoginActivity)
                                    AuthPreference(this@LoginActivity).saveAuthData(data.data)
                                    showToast(
                                        data.message.toString(),
                                        this@LoginActivity
                                    )
                                    Intent(this@LoginActivity, HomeActivity::class.java).apply {
                                        startActivity(this)
                                    }
                                    viewState(isLoading = false, showView = true)
                                    finish()
                                }
                                is Resource.Error<*> -> {
                                    showToast(
                                        GlobalUtils.getErrorMessageFromJSON(data.message.toString()),
                                        this@LoginActivity
                                    )
                                    viewState(isLoading = false, showView = true)
                                    livedata.removeObservers(this@LoginActivity)
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    private fun viewState(showView: Boolean, isLoading:Boolean) {
        binding.mainLayout.visibility = if(showView) View.VISIBLE else View.GONE
        binding.viewLoading.loadingLayout.visibility = if(isLoading) View.VISIBLE else View.GONE
    }
}