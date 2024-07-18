# climatecity
Organising CMPI6 data by city

## FAQ
### Who are you?
[A Lecturer in Data Science at the University of Exeter](https://computerscience.exeter.ac.uk/people/profile/index.php?web_id=ra414)
### What is this?
This is a tool to let you search for future climate predictions for your city or town.
### Why?
Similar tools exist, like the [IPCC atlas](https://interactive-atlas.ipcc.ch/regional-information#eyJ0eXBlIjoiQVRMQVMiLCJjb21tb25zIjp7ImxhdCI6OTc3MiwibG5nIjo0MDA2OTIsInpvb20iOjQsInByb2oiOiJFUFNHOjU0MDMwIiwibW9kZSI6ImNvbXBsZXRlX2F0bGFzIn0sInByaW1hcnkiOnsic2NlbmFyaW8iOiJzc3A1ODUiLCJwZXJpb2QiOiIyIiwic2Vhc29uIjoieWVhciIsImRhdGFzZXQiOiJDTUlQNiIsInZhcmlhYmxlIjoidGFzIiwidmFsdWVUeXBlIjoiQU5PTUFMWSIsImhhdGNoaW5nIjoiU0lNUExFIiwicmVnaW9uU2V0IjoiYXI2IiwiYmFzZWxpbmUiOiJwcmVJbmR1c3RyaWFsIiwicmVnaW9uc1NlbGVjdGVkIjpbXX0sInBsb3QiOnsiYWN0aXZlVGFiIjoicGx1bWUiLCJtYXNrIjoibm9uZSIsInNjYXR0ZXJZTWFnIjpudWxsLCJzY2F0dGVyWVZhciI6bnVsbCwic2hvd2luZyI6ZmFsc2V9fQ==), but I couldn't find anything that explicitly gives you the prediction for a particular town. Since most people know the name of their town but not its lat/lon grid box, this seemed like something which ought to exist!
### What is the data?
The climate predictions are data from CMIP6 which I got from [Copernicus](https://cds.climate.copernicus.eu/cdsapp#!/dataset/projections-climate-atlas?tab=overview). The list of towns and cities comes from [Geonames](https://download.geonames.org/export/dump/cities15000.zip).
### My town isn't on here!
I used Geonames' list of towns and cities with over 15000 population, it's possible your town is too small.
### What does SSP585/370/245/126 mean?
Climate projections are made according to different scenarios, from a full net zero transition (SSP126) to fossil fuel driven growth (SSP585). See [here](https://www.dkrz.de/en/communication/climate-simulations/cmip6-en/the-ssp-scenarios) for more detail.
### City A and City B give the same results!
The grid boxes for the climate models are fairly big. If two places are nearby they might fall in the same box and their predictions will be the same.
### Why didn't you...?
This is a small project I did because I needed this data to be available and searchable by town. If you are a climate scientist or other expert and you want to help improve it, please get in touch.
