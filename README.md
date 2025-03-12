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

<h3>3/10:</h3>
<p>
  I started this GitHub repo <br>
  With the rib file I have the ASNs of the IPv6 addresses so I should find the repeated IIDs and match it to an ASN<br>
  Thoughts - Go through all the unique repeated IIDs and find their /48? With that /48 then find the ASN? 
</p>

<h3>3/11:</h3>
<p>
  Went through with my thoughts from yesterday. I compared my list of unique /48s with the list of the outputs<br>
  from the rib file from the routeviews project. With the list, I removed all the repeats and ran it through<br>
  whois from cymru. Next goal: get counts of IPs by ASN and counts of IPs by country code.
</p>
