package com.bangkit.yourney.ui.intro

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import androidx.viewpager.widget.ViewPager
import com.bangkit.yourney.R
import com.bangkit.yourney.databinding.ActivityIntroBinding
import com.bangkit.yourney.domain.model.Favorite
import com.bangkit.yourney.domain.model.Slider
import com.bangkit.yourney.ui.authentication.LoginActivity
import com.bangkit.yourney.ui.authentication.RegisterActivity

class IntroActivity : AppCompatActivity() {
    private lateinit var binding: ActivityIntroBinding
    private lateinit var sliderAdapter: IntroViewPagerAdapter
    private val sliderList = ArrayList<Slider>()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityIntroBinding.inflate(layoutInflater)
        setContentView(binding.root)

        sliderList.add(Slider("Login With Your Social Media Account", "With your login using social media, we can predict your destination recommendations.", R.drawable.ic_login_black))
        sliderList.add(Slider("We Predict Your Favorite Destinations", "We use an A.I to predict your most favorite destination to visit.", R.drawable.ic_sparkle_black))
        sliderList.add(Slider("Get Your Tour Package", "We give you a tour package suitable for your.", R.drawable.ic_package_search_black_bold))
        sliderList.add(Slider("Enjoy Your Holiday", "We give you a tour package suitable for your.", R.drawable.ic_beach_with_umbrella_black))

        sliderAdapter = IntroViewPagerAdapter(this, sliderList)

        with(binding) {
            viewPager.adapter = sliderAdapter
            viewPager.addOnPageChangeListener(viewListener)
            btnMasuk.setOnClickListener {
                Intent(this@IntroActivity, LoginActivity::class.java).apply {
                    startActivity(this)
                }
                finish()
            }
            btnDaftar.setOnClickListener {
                Intent(this@IntroActivity, RegisterActivity::class.java).apply {
                    startActivity(this)
                }
                finish()
            }
        }
    }

    private var viewListener: ViewPager.OnPageChangeListener = object : ViewPager.OnPageChangeListener {
        override fun onPageScrolled(
            position: Int,
            positionOffset: Float,
            positionOffsetPixels: Int
        ) {
        }

        override fun onPageSelected(position: Int) {
            // we are calling our dots method to
            // change the position of selected dots.

            // on below line we are checking position and updating text view text color.
            selectedIndicator(position+1)
        }

        // below method is use to check scroll state.
        override fun onPageScrollStateChanged(state: Int) {}
    }

    private fun selectedIndicator(selected: Int) {
        binding.idTVSlideOne.setTextColor(if(selected == 1) resources.getColor(R.color.cyan) else resources.getColor(R.color.grey))
        binding.idTVSlideTwo.setTextColor(if(selected == 2) resources.getColor(R.color.cyan) else resources.getColor(R.color.grey))
        binding.idTVSlideThree.setTextColor(if(selected == 3) resources.getColor(R.color.cyan) else resources.getColor(R.color.grey))
        binding.idTVSlideFour.setTextColor(if(selected == 4) resources.getColor(R.color.cyan) else resources.getColor(R.color.grey))
    }
}