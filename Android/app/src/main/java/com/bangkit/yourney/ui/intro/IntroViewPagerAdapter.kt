package com.bangkit.yourney.ui.intro

import android.content.Context
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageView
import android.widget.TextView
import androidx.constraintlayout.widget.ConstraintLayout
import androidx.viewpager.widget.PagerAdapter
import com.bangkit.yourney.R
import com.bangkit.yourney.domain.model.Favorite
import com.bangkit.yourney.domain.model.Slider

class IntroViewPagerAdapter(
    val context: Context,
    val sliderList: ArrayList<Slider>
): PagerAdapter() {

    override fun getCount(): Int {
        // on below line we are returning
        // the size of slider list
        return sliderList.size
    }

    override fun isViewFromObject(view: View, `object`: Any): Boolean {
        // inside isViewFromobject method we are
        // returning our Relative layout object.
        // inside isViewFromobject method we are
        // returning our Relative layout object.
        return view === `object` as ConstraintLayout
    }

    override fun instantiateItem(container: ViewGroup, position: Int): Any {
        // in this method we will initialize all our layout
        // items and inflate our layout file as well.
        // in this method we will initialize all our layout
        // items and inflate our layout file as well.
        val layoutInflater: LayoutInflater =
            context.getSystemService(Context.LAYOUT_INFLATER_SERVICE) as LayoutInflater

        // below line is use to inflate the
        // layout file which we created.

        // below line is use to inflate the
        // layout file which we created.
        val view: View = layoutInflater.inflate(R.layout.slider_item, container, false)

        // on below line we are initializing our image view,
        // heading text view and description text view with their ids.
        val imageView: ImageView = view.findViewById(R.id.iv_intro)
        val sliderHeadingTV: TextView = view.findViewById(R.id.tv_lbl_text)
        val sliderDescTV: TextView = view.findViewById(R.id.tv_lbl_text1)

        // on below line we are setting data to our text view
        // and image view on below line.
        val sliderData: Slider = sliderList.get(position)
        sliderHeadingTV.text = sliderData.title
        sliderDescTV.text = sliderData.subtitle
        imageView.setImageResource(sliderData.image!!)

        // on below line we are adding our view to container.
        container.addView(view)

        // on below line we are returning our view.
        return view
    }

    override fun destroyItem(container: ViewGroup, position: Int, `object`: Any) {
        // this is a destroy view method
        // which is use to remove a view.
        // this is a destroy view method
        // which is use to remove a view.
        container.removeView(`object` as ConstraintLayout)
    }
}