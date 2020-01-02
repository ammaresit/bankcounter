package com.example.bankcounter;

import androidx.appcompat.app.AppCompatActivity;

import android.annotation.SuppressLint;
import android.content.Context;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;

import cz.msebera.android.httpclient.util.EntityUtils;
import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;

public class MainActivity extends AppCompatActivity {

    Button btnSira;
    TextView txtGise1, txtGise2, txtSira, txtSiranizGeldi;
    String gise1="asd", gise2="asd";
    Thread threadRead;

    final Context context = this;

    final String URLread = "http://192.168.137.1:80/read";
    final String URLwrite = "http://192.168.137.1:80/write";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // LAYOUT WIDGETS ASSIGNMENT!
        btnSira = findViewById(R.id.btnSira);
        txtGise1 = findViewById(R.id.txtGise1);
        txtGise2 = findViewById(R.id.txtGise2);
        txtSira = findViewById(R.id.txtSira);
        txtSiranizGeldi = findViewById(R.id.txtSiranizGeldi);

        // butonun click listener metodu ve detayını işler!
        setListener();

        startThread();

    } // onCreate


    private void setListener() {

        // SIRA ALMA METODU !!
        final OkHttpClient clientWrite = new OkHttpClient();

        assert btnSira != null;
        btnSira.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(final View view) {

                // ilk kayittaki sirayi sorgulamak adina!
                String URLreadId = URLread+"?id=1";

                final Request request = new Request.Builder().url(URLreadId).build();
                clientWrite.newCall(request).enqueue(new Callback() {
                    @Override
                    public void onResponse(Call call, Response response) throws IOException {
                        if(response.isSuccessful()){

                            JSONObject myResponse = null;
                            String sira = null;
                            try {
                                myResponse = new JSONObject(response.body().string());
                                sira = myResponse.getString("sira");
                            } catch (JSONException e) {
                                e.printStackTrace();
                            } // catch0

                            int a = Integer.parseInt(sira);
                            a += 1;
                            final int finalA = a;

                            MainActivity.this.runOnUiThread(new Runnable() {
                                @SuppressLint("Assert")
                                @Override
                                public void run() {

                                    assert false;
                                    txtSira.setText(String.valueOf(finalA));
                                } // catch2
                            });

                            // Güncellenen sirayi veritabanına yazan method!
                            siraAl(clientWrite, a);


                        } // if0

                    } // onResponse
                    @Override
                    public void onFailure(Call call, IOException e) {
                        Log.e("Error setListener Request: ", "Error onFailure: "+e.getMessage());
                    } // onFailure
                });

            } // onClick
        }); // setOnClickListener

    } // setListener

    private void siraAl(OkHttpClient clientWrite, int sira) {

        String i = "1";
        String s = String.valueOf(sira);
        String g1 = txtGise1.getText().toString();
        String g2 = txtGise2.getText().toString();

        String URLwriteguncelle = URLwrite+"?id="+i+"&sira="+s+"&gise1="+g1+"&gise2="+g2;

        Request rq = new Request.Builder().url(URLwriteguncelle).build();
        clientWrite.newCall(rq).enqueue(new Callback() {
            @Override
            public void onResponse(Call call, Response response) throws IOException {

                if(response.isSuccessful()){
                    Log.d("SIRA AL:", "Sira Basariyla Alindi!");
                }

            } // onResponse
            @Override
            public void onFailure(Call call, IOException e) {
                Log.e("Error SiraAl: ", "Error Sira Al: "+e.getMessage());
            } // onFailure
        });

        runOnUiThread(new Runnable() {
            @Override
            public void run() {

                btnSira.setEnabled(false);
            }
        });

    } // siraAl


    public void startThread() {

        ExampleThread thread = new ExampleThread(1800);
        thread.start();

    } // startThread

    // Example Thread Class
    class ExampleThread extends Thread {

        int seconds;

        ExampleThread(int seconds) {

            this.seconds = seconds;
        }

        @Override
        public void run() {

            for (int i=0; i<seconds; ++i){

                Log.d("MainActivity: ", "ExampleThread: "+i);

                try {

                    // FARKLI ID'ye SAHİP BİR KAYDA ULAŞILMAK İSTENİRSE ID DEGERI ONA GORE DUZENLENMELIDIR!
                    final String URLread1 = URLread+"?id=1";
                    final OkHttpClient clientRead = new OkHttpClient();

                    Request rq = new Request.Builder().url(URLread1).build();
                    clientRead.newCall(rq).enqueue(new Callback() {
                        @SuppressLint("SetTextI18n")
                        @Override
                        public void onResponse(Call call, final Response response) throws IOException {

                            if (response.isSuccessful()) {
                                assert response.body() != null;
                                try {
                                    final JSONObject j = new JSONObject(response.body().string());

                                    runOnUiThread(new Runnable() {
                                        @Override
                                        public void run() {

                                            try {
                                                String gise1 = j.getString("gise1");
                                                txtGise1.setText(gise1);
                                                String gise2 = j.getString("gise2");
                                                txtGise2.setText(gise2);
                                            } catch (JSONException e) {
                                                Log.e("Error JSONObject: ",
                                                        "threadRead JSONObject getString Error: " + e.getMessage());
                                            } // catch0

                                            if (txtGise1.getText().toString().equals(txtSira.getText().toString())) {
                                                txtSiranizGeldi.setText("Gise 1'e İlerleyiniz!");
                                                txtSiranizGeldi.setVisibility(View.VISIBLE);
                                            } else if (txtGise2.getText().toString().equals(txtSira.getText().toString())) {
                                                txtSiranizGeldi.setText("Gise 2'ye İlerleyiniz!");
                                                txtSiranizGeldi.setVisibility(View.VISIBLE);
                                            } // else if

                                        }
                                    });

                                } catch (JSONException e) {
                                    Log.e("Error JSONObject: ",
                                            "threadRead JSONObject create Error: " + e.getMessage());
                                } // catch1
                            } // if response is successful
                        } // onResponse

                        @Override
                        public void onFailure(Call call, IOException e) {
                            Log.e("Error onFailure: ", "threadRead Error: " + e.getMessage());
                        } // onFailure
                    });
                } catch (Exception e) {
                    e.printStackTrace();
                } // catch2

                try {
                    Thread.sleep(500);
                } catch (InterruptedException e) {
                    Log.e("Thread Run Error: ", "ExampleThread run Error: "+e.getMessage());
                }

            } // for0

        }
    } // ExampleThread


} // end of MainActivity class