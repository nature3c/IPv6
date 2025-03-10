<h1>
  Code I used to look into IPv6 addresses
</h1>
<p>
  Goals: Find why IIDs repeat in IPv6 addresses and fix that<br>
</p>

<h3>So far since September</h3>
<p>
  Made code to take IPv6 addresses with high entropy and sort them by how many times that IID appears<br>
  Proved that this is a problem in at least 3 ISPs, so now find how many more are affected.<br>
  Very fun but processing this much data takes forever. Talking about data, it's from IPv6 Observatory<br>
  Working with Erik Rye is the best.
</p>

<h3>3/5:</h3>
<p>
  I started this GitHub repo <br>
  With the rib file I have the ASNs of the IPv6 addresses so I should find the repeated IIDs and match it to an ASN<br>
  Thoughts - Go through all the unique repeated IIDs and find their /48? With that /48 then find the ASN? 
</p>
