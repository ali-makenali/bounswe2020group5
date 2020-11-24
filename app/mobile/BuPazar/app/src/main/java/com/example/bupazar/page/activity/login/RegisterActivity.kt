package com.example.bupazar.page.activity.login

import android.content.Intent
import android.os.Bundle
import android.view.View
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.example.bupazar.R
import com.example.bupazar.model.LoginRequest
import com.example.bupazar.model.RegisterRequest
import com.example.bupazar.page.activity.home.HomepageActivity
import com.example.bupazar.service.RestApiService
import com.google.gson.annotations.SerializedName
import kotlinx.android.synthetic.main.fragment_register.*
import kotlinx.android.synthetic.main.fragment_register.buttonRegister
import kotlinx.android.synthetic.main.fragment_register.passwordEditTextView
import kotlinx.android.synthetic.main.fragment_register.usernameEditTextView

class RegisterActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.fragment_register)
        progressBarHide()

        buttonRegister.setOnClickListener() {
            progressBarShow()

            if (usernameTextView.text.isEmpty() || passwordEditTextView.text.isEmpty() || mailEditTextView.text.isEmpty() || firstNameEditTextView.text.isEmpty()
                || surnameEditTextView.text.isEmpty()){
                Toast.makeText(this@RegisterActivity,"All the blanks should be filled", Toast.LENGTH_SHORT).show()
            }
            else {
                val apiService = RestApiService()
                val userInfo = RegisterRequest(
                    userEmail = mailEditTextView.text.toString(),
                    username = usernameEditTextView.text.toString(),
                    userFirstName = firstNameEditTextView.text.toString(),
                    userLastName = surnameEditTextView.text.toString(),
                    userIsCustomer = true,
                    userIsVendor = false,
                    userPassword = passwordEditTextView.text.toString(),
                    userAddress = "address",
                )
                apiService.userRegister(userInfo) {
                    if(it?.username == null){
                        progressBarHide()
                        Toast.makeText(this@RegisterActivity,"Register credentials are not valid" , Toast.LENGTH_SHORT).show()
                    }
                    else {
                        progressBarHide()
                        Toast.makeText(this@RegisterActivity,"Your registration is completed, login is being made" , Toast.LENGTH_SHORT).show()
                        var intent = Intent(this, HomepageActivity::class.java)
                        startActivity(intent)
                    }
                }
            }
        }
    }

    private fun progressBarShow(){
        progress_Bar.visibility = View.VISIBLE
    }
    private fun progressBarHide(){
        progress_Bar.visibility = View.INVISIBLE
    }
}