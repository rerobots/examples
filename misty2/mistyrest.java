// This is free software, released under the Apache License, Version 2.0.
// You may obtain a copy of the License at https://www.apache.org/licenses/LICENSE-2.0
// Copyright (c) 2020 rerobots, Inc.

import java.io.*;
import java.net.*;


public class RerobotsExample {
    public static void main( String[] args) throws Exception {
        URL mpurl = new URL("{{ mistyhttps }}" + "/api/battery");
        URLConnection uc = mpurl.openConnection();
        BufferedReader br = new BufferedReader(new InputStreamReader(uc.getInputStream()));
        String inputLine = br.readLine();
        System.out.println(inputLine);
        br.close();
    }
}
