package com.bangkit.yourney.ui.main.home

import android.R.id.button1
import android.content.Intent
import android.os.Bundle
import android.text.Editable
import android.text.TextWatcher
import android.util.Log
import android.view.*
import android.widget.Toast
import androidx.appcompat.widget.PopupMenu
import androidx.fragment.app.Fragment
import androidx.recyclerview.widget.StaggeredGridLayoutManager
import com.bangkit.yourney.R
import com.bangkit.yourney.data.Resource
import com.bangkit.yourney.data.sharedpreference.AuthPreference
import com.bangkit.yourney.data.sharedpreference.IntroPreference
import com.bangkit.yourney.databinding.FragmentHomeBinding
import com.bangkit.yourney.ui.authentication.LoginActivity
import com.bangkit.yourney.ui.main.MainViewModel
import com.bangkit.yourney.ui.main.detail.DestinationDetailActivity
import com.bangkit.yourney.utils.Constanta
import com.bangkit.yourney.utils.GlobalUtils
import org.koin.androidx.viewmodel.ext.android.viewModel


class HomeFragment : Fragment() {
    private var _binding: FragmentHomeBinding? = null
    private val binding get() = _binding!!
    private val viewModel: MainViewModel by viewModel()
    private var currentPosition = 0
    private lateinit var destinationListAdapter: DestinationListAdapter
    private lateinit var listener: ToggleListener

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentHomeBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        if (activity != null) {
            listener = requireActivity() as ToggleListener
            initDestinationData()
            with(binding) {
                tietSearch.addTextChangedListener(object : TextWatcher {
                    override fun afterTextChanged(s: Editable) {
                        Log.d("TAG_TEXT_AFTER_CHANGE", s.toString())
                        if (s.isNotEmpty())
                            searchDestination(s.toString())
                        else
                            getAllDestination()
                    }

                    override fun beforeTextChanged(
                        s: CharSequence, start: Int,
                        count: Int, after: Int
                    ) {
                        Log.d("TAG_TEXT_BEFORE_CHANGE", s.toString())
                    }

                    override fun onTextChanged(
                        s: CharSequence, start: Int,
                        before: Int, count: Int
                    ) {
                        Log.d("TAG_TEXT_IN_CHANGE", s.toString())
//                    if (s.isNotEmpty()) tietSearch.setText("")
                    }
                })
                ivToggle.setOnClickListener {
                    val popup = PopupMenu(requireContext(), it)
                    popup.menuInflater
                        .inflate(R.menu.filter_menu, popup.menu)

                    popup.setOnMenuItemClickListener { item ->
                        viewState(isLoading = true, isError = false, isEmpty =  false, showView = false)
                        var filter = "all"
                        when (item.itemId) {
                            R.id.btn_filter_pantai -> {
                                filter = "pantai"
                            }
                            R.id.btn_filter_gunung -> {
                                filter = "gunung"
                            }
                            R.id.btn_filter_kuliner -> {
                                filter = "kuliner"
                            }
                            R.id.btn_show_all -> {
                                getAllDestination()
                            }
                        }
                        if(filter != "all") {
                            val livedata = viewModel.filterDestination(
                                AuthPreference(requireContext()).getToken,
                                filter
                            )
                            livedata.observe(viewLifecycleOwner) { data ->
                                if (data != null) {
                                    when (data) {
                                        is Resource.Loading<*> -> {
                                            Log.d("TAG_LOADING", "JUST LOADING")
                                        }
                                        is Resource.Success<*> -> {
                                            Log.d("TAG_SUCCESS", data.data.toString())
                                            destinationListAdapter.setData(data.data)
                                            livedata.removeObservers(viewLifecycleOwner)
                                            GlobalUtils.showToast(
                                                data.message.toString(),
                                                requireContext()
                                            )
                                            viewState(
                                                isLoading = false,
                                                isError = false,
                                                isEmpty = (data.data?.isEmpty() == true),
                                                showView = true
                                            )
                                        }
                                        is Resource.Error<*> -> {
                                            Log.d("TAG_ERROR", data.message.toString())
                                            if (data.data == null)
                                                viewState(
                                                    isLoading = false,
                                                    showView = false,
                                                    isError = false,
                                                    isEmpty = true
                                                )
                                            else
                                                viewState(
                                                    isLoading = false,
                                                    showView = false,
                                                    isError = true,
                                                    isEmpty = false
                                                )

                                            GlobalUtils.showToast(
                                                data.message.toString(),
                                                requireContext()
                                            )
                                            livedata.removeObservers(viewLifecycleOwner)
                                        }
                                    }
                                }
                            }
                        }
                        true
                    }

                    popup.show()
                }
            }
        }
    }

    private fun initDestinationData() {
        destinationListAdapter = DestinationListAdapter()
        destinationListAdapter.onItemClick = {
            Intent(requireContext(), DestinationDetailActivity::class.java).apply {
                this.putExtra(Constanta.DESTINATION_DATA, it)
                startActivity(this)
            }
        }
        with(binding.rvDestination) {
            layoutManager = StaggeredGridLayoutManager(2, StaggeredGridLayoutManager.VERTICAL)
            (layoutManager as StaggeredGridLayoutManager).invalidateSpanAssignments()
            adapter = destinationListAdapter
//            (layoutManager as StaggeredGridLayoutManager).gapStrategy = StaggeredGridLayoutManager.GAP_HANDLING_NONE
            setHasFixedSize(true)
        }
        getAllDestination()
    }

    private fun getAllDestination() {
        viewState(isLoading = true, isError = false, isEmpty =  false, showView = false)
        val livedata = viewModel.allDestination(AuthPreference(requireContext()).getToken)
        livedata.observe(viewLifecycleOwner) { data ->
            if (data != null) {
                when (data) {
                    is Resource.Loading<*> -> {
                        Log.d("TAG_LOADING", "JUST LOADING")
                    }
                    is Resource.Success<*> -> {
                        Log.d("TAG_SUCCESS", data.data.toString())
                        destinationListAdapter.setData(data.data)
                        destinationListAdapter.firstItem = {
                            currentPosition = destinationListAdapter.getPosition()
                            binding.rvDestination.smoothScrollToPosition(currentPosition)
                            if(IntroPreference(requireContext()).isFirstimeTutorial) {
                                listener.getCurrentPosition(currentPosition)
                                listener.showTutors()
                                IntroPreference(requireContext()).saveStatusTutor(false)
                            }
                        }
                        viewState(isLoading = false, isError = false, isEmpty = (data.data?.isEmpty() == true), showView = true)
                        livedata.removeObservers(viewLifecycleOwner)
                    }
                    is Resource.Error<*> -> {
                        if(data.data == null)
                            viewState(isLoading = false, showView = false, isError = false, isEmpty = true)
                        else
                            viewState(isLoading = false, showView = false, isError = true, isEmpty = false)
                        if (data.message?.contains("msg") == true) {
                            Intent(requireContext(), LoginActivity::class.java).apply {
                                startActivity(this)
                            }
                            GlobalUtils.showToast("Your session has expired!", requireContext())
                            requireActivity().finish()
                        } else {
                            GlobalUtils.showToast(if(data.message?.contains("{") == true)
                                GlobalUtils.getErrorMessageFromJSON("data.message") else "UnExcepted Error",
                                requireContext()
                            )
                        }
                        livedata.removeObservers(viewLifecycleOwner)
                    }
                }
            }
        }
    }

    private fun searchDestination(key: String) {
        viewState(isLoading = true, isError = false, isEmpty = false, showView = false)
        val livedata = viewModel.searchDestination(AuthPreference(requireContext()).getToken, key)
        livedata.observe(viewLifecycleOwner) { data ->
            if (data != null) {
                when (data) {
                    is Resource.Loading<*> -> {
                        Log.d("TAG_LOADING", "JUST LOADING")
                    }
                    is Resource.Success<*> -> {
                        Log.d("TAG_SUCCESS", data.data.toString())
                        binding.rvDestination.visibility = View.VISIBLE
                        binding.viewError.viewErrorLayout.visibility = View.GONE
                        destinationListAdapter.setData(data.data)
                        livedata.removeObservers(viewLifecycleOwner)
                        viewState(isLoading = false, isError = false, isEmpty = (data.data?.isEmpty() == true), showView = true)
                    }
                    is Resource.Error<*> -> {
                        if(data.data == null)
                            viewState(isLoading = false, showView = false, isError = false, isEmpty = true)
                        else
                            viewState(isLoading = false, showView = false, isError = true, isEmpty = false)

                        GlobalUtils.showToast(
                            data.message.toString(),
                            requireContext()
                        )
                        livedata.removeObservers(viewLifecycleOwner)
                    }
                }
            }
        }
    }

    private fun viewState(showView: Boolean, isLoading:Boolean, isError: Boolean, isEmpty: Boolean) {
        binding.rvDestination.visibility = if(showView) View.VISIBLE else View.GONE
        binding.viewLoading.loadingLayout.visibility = if(isLoading) View.VISIBLE else View.GONE
        binding.viewError.viewErrorLayout.visibility = if(isError) View.VISIBLE else View.GONE
        binding.viewEmpty.emptyLayout.visibility = if(isEmpty) View.VISIBLE else View.GONE
    }

    interface ToggleListener {
        fun onOpenClick()
        fun showLoading()
        fun hideLoading()
        fun showTutors()
        fun getFirstView(firstView: View)
        fun getCurrentPosition(position: Int)
    }
}