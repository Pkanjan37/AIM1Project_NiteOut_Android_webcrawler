package com.aim1.services;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

/**
 * Created by root on 18.01.18.
 */

public class NiteoutServiceFactory {

    private static NiteoutService _service;

    public static NiteoutService getService(){
        if(_service == null){
            Gson gson = new GsonBuilder()
                    .setLenient()
                    .create();

            Retrofit retrofit = new Retrofit.Builder()
                    .baseUrl(UrlConstant.BASE_URL)
                    .addConverterFactory(GsonConverterFactory.create(gson))
                    .build();

            _service = retrofit.create(NiteoutService.class);
        }
        return _service;
    }
}
