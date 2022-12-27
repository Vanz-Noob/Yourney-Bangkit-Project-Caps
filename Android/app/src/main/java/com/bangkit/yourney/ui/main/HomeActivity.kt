package com.bangkit.yourney.ui.main

import android.content.Intent
import android.graphics.Typeface
import android.os.Bundle
import android.view.View
import android.widget.TextView
import androidx.appcompat.app.ActionBarDrawerToggle
import androidx.appcompat.app.AppCompatActivity
import androidx.cardview.widget.CardView
import androidx.fragment.app.Fragment
import androidx.recyclerview.widget.RecyclerView
import com.bangkit.yourney.R
import com.bangkit.yourney.data.sharedpreference.AuthPreference
import com.bangkit.yourney.databinding.ActivityHomeBinding
import com.bangkit.yourney.ui.authentication.LoginActivity
import com.bangkit.yourney.ui.main.favorite.FavoriteDestinationFragment
import com.bangkit.yourney.ui.main.home.HomeFragment
import com.bangkit.yourney.ui.user.UserSettingActivity
import com.bangkit.yourney.utils.DialogUtils
import com.bangkit.yourney.utils.GlobalUtils.showToast
import com.bangkit.yourney.utils.ImageViewUtils.loadImageFromServer
import com.bangkit.yourney.utils.ImageViewUtils.loadImageFromServerWithAuth
import com.bumptech.glide.load.model.GlideUrl
import com.bumptech.glide.load.model.LazyHeaders
import com.getkeepsafe.taptargetview.TapTarget
import com.getkeepsafe.taptargetview.TapTargetSequence
import de.hdodenhof.circleimageview.CircleImageView

class HomeActivity : AppCompatActivity(), HomeFragment.ToggleListener {
    private lateinit var binding: ActivityHomeBinding
    private var currentSelectItemId = R.id.btn_nav_home
    private lateinit var dialogUtils: DialogUtils
    private lateinit var firstView: View
    private var currentPosition = 0

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityHomeBinding.inflate(layoutInflater)
        setContentView(binding.root)
        dialogUtils = DialogUtils()
        dialogUtils.setCustomDialog(this, R.layout.dialog_loading)
        val toggle = ActionBarDrawerToggle(
            this,
            binding.drawerLayout,
            null,
            R.string.navigation_drawer_open,
            R.string.navigation_drawer_close
        )
        binding.drawerLayout.addDrawerListener(toggle)
        toggle.syncState()
        setFragmentView(savedInstanceState)
        initUser()
    }

    private fun initUser() {
        val data = AuthPreference(this).authData
        if(data != null) {
            binding.navView.getHeaderView(0).findViewById<TextView>(R.id.tv_username).text = data.username
            binding.navView.getHeaderView(0).findViewById<TextView>(R.id.tv_email).text = data.email

            if(data.avatar == "null" || data.avatar == "" || data.avatar == null) {
                binding.navView.getHeaderView(0).findViewById<CircleImageView>(R.id.nav_drawer_img_avatar).setImageResource(R.drawable.default_user_image)
            } else {
                binding.navView.getHeaderView(0).findViewById<CircleImageView>(R.id.nav_drawer_img_avatar).loadImageFromServer(data.avatar)
            }
        }
    }

    private fun setFragmentView(savedInstanceState: Bundle?) {
        val homeFragment = HomeFragment()
        val favoriteFragment = FavoriteDestinationFragment()
//        val userSettingFragment = UserSettingFragment()
//        val accountFragment = AccountFragment()

        if (savedInstanceState != null) {
            currentSelectItemId = savedInstanceState.getInt(SAVED_STATE_CURRENT_TAB_KEY)
        }

        when(currentSelectItemId) {
            R.id.btn_nav_home -> setCurrentFragment(homeFragment, currentSelectItemId)
        }

        binding.navView.setNavigationItemSelectedListener {
            when (it.itemId) {
                R.id.btn_nav_account -> Intent(this@HomeActivity, UserSettingActivity::class.java).apply {
                    startActivity(this)
                }
//                R.id.btn_nav_history -> showToast("Menu belum selesai!", this)
//                R.id.btn_nav_setting -> showToast("Menu belum selesai!", this)
                R.id.btn_nav_help -> {
                    binding.drawerLayout.closeDrawer(binding.navView)
                    binding.navHostFragment.findViewById<RecyclerView>(R.id.rv_destination).smoothScrollToPosition(currentPosition)
                    showTutors()
                }
                R.id.btn_nav_signout -> {
                    AuthPreference(this).saveAuthData(null)
                    Intent(this, LoginActivity::class.java).apply {
                        startActivity(this)
                    }
                    finish()
                }
                else -> throw AssertionError()
            }
            true
        }

        binding.bnvMain.setOnItemSelectedListener {
            when (it.itemId) {
                R.id.btn_nav_home -> setCurrentFragment(homeFragment, it.itemId)
                R.id.btn_nav_favorite -> setCurrentFragment(favoriteFragment, it.itemId)
                R.id.btn_nav_menu -> binding.drawerLayout.openDrawer(binding.navView)
                else -> throw AssertionError()
            }
            true
        }
    }

    override fun getFirstView(firstView: View) {
        this.firstView = firstView
    }

    override fun getCurrentPosition(position: Int) {
        this.currentPosition = position
    }

    override fun showTutors() {
//        if(!this::firstView.isInitialized)
//            this.firstView = firstView
        TapTargetSequence(this)
            .targets(
                TapTarget.forView(binding.bnvMain.findViewById(R.id.btn_nav_home), "Home", "See all destination or you can filter or search a destination")
                    .outerCircleColor(R.color.black)
                    .outerCircleAlpha(0.9f)
                    .targetCircleColor(R.color.white)
                    .titleTextSize(24)
                    .titleTextColor(R.color.white)
                    .descriptionTextSize(16)
                    .descriptionTextColor(R.color.white)
                    .textColor(R.color.white)
                    .textTypeface(Typeface.SANS_SERIF)
                    .dimColor(R.color.black)
                    .drawShadow(true)
                    .cancelable(false)
                    .tintTarget(true)
                    .transparentTarget(true)
                    .targetRadius(60),
                TapTarget.forView(binding.bnvMain.findViewById(R.id.btn_nav_favorite), "Saved", "All destination saved/favorite, you can add a destination that you like")
                    .outerCircleColor(R.color.black)
                    .outerCircleAlpha(0.9f)
                    .targetCircleColor(R.color.white)
                    .titleTextSize(24)
                    .titleTextColor(R.color.white)
                    .descriptionTextSize(16)
                    .descriptionTextColor(R.color.white)
                    .textColor(R.color.white)
                    .textTypeface(Typeface.SANS_SERIF)
                    .dimColor(R.color.black)
                    .drawShadow(true)
                    .cancelable(false)
                    .tintTarget(true)
                    .transparentTarget(true)
                    .targetRadius(60),
                TapTarget.forView(binding.bnvMain.findViewById(R.id.btn_nav_menu), "Menu", "You can open sidebar from this menu")
                    .outerCircleColor(R.color.black)
                    .outerCircleAlpha(0.9f)
                    .targetCircleColor(R.color.white)
                    .titleTextSize(24)
                    .titleTextColor(R.color.white)
                    .descriptionTextSize(16)
                    .descriptionTextColor(R.color.white)
                    .textColor(R.color.white)
                    .textTypeface(Typeface.SANS_SERIF)
                    .dimColor(R.color.black)
                    .drawShadow(true)
                    .cancelable(false)
                    .tintTarget(true)
                    .transparentTarget(true)
                    .targetRadius(60),
                TapTarget.forView(binding.navHostFragment.findViewById<CardView>(R.id.cardView), "Search", "You can search and filter from here")
                    .outerCircleColor(R.color.black)
                    .outerCircleAlpha(0.9f)
                    .targetCircleColor(R.color.white)
                    .titleTextSize(24)
                    .titleTextColor(R.color.white)
                    .descriptionTextSize(16)
                    .descriptionTextColor(R.color.white)
                    .textColor(R.color.white)
                    .textTypeface(Typeface.SANS_SERIF)
                    .dimColor(R.color.black)
                    .drawShadow(true)
                    .cancelable(true)
                    .tintTarget(true)
                    .transparentTarget(true)
                    .targetRadius(15),
//                TapTarget.forView(this.firstView, "Destination", "You can select your favorite destination")
//                    .outerCircleColor(R.color.black)
//                    .outerCircleAlpha(0.9f)
//                    .targetCircleColor(R.color.white)
//                    .titleTextSize(24)
//                    .titleTextColor(R.color.white)
//                    .descriptionTextSize(15)
//                    .descriptionTextColor(R.color.white)
//                    .textColor(R.color.white)
//                    .textTypeface(Typeface.SANS_SERIF)
//                    .dimColor(R.color.black)
//                    .drawShadow(false)
//                    .cancelable(true)
//                    .tintTarget(false)
//                    .transparentTarget(true)
//                    .targetRadius(120)
            ).listener(object : TapTargetSequence.Listener {
                override fun onSequenceFinish() {
                    showToast("Finish Tutor", this@HomeActivity)
                }

                override fun onSequenceStep(lastTarget: TapTarget, targetClicked: Boolean) {
//                    showToast("Stop", this@HomeActivity)
                }

                override fun onSequenceCanceled(lastTarget: TapTarget) {
//                    showToast("Cancel", this@HomeActivity)
                }
            }).start()
    }

    private fun setCurrentFragment(fragment: Fragment, itemId: Int) {
        currentSelectItemId = itemId
        supportFragmentManager.beginTransaction().replace(R.id.nav_host_fragment, fragment).disallowAddToBackStack().commit()
    }

    override fun onSaveInstanceState(outState: Bundle) {
        super.onSaveInstanceState(outState)
        outState.putInt(SAVED_STATE_CURRENT_TAB_KEY, currentSelectItemId)
    }

    override fun onOpenClick() {
        binding.drawerLayout.openDrawer(binding.navView)
    }

    override fun showLoading() {
        dialogUtils.showDialog()
    }

    override fun hideLoading() {
        dialogUtils.closeDialog()
    }

    override fun onResume() {
        super.onResume()
        initUser()
    }

    companion object {
        const val SAVED_STATE_CURRENT_TAB_KEY = "CurrentTabKey"
    }
}