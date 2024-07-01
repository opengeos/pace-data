import hypercoast
import earthaccess
import leafmap
import datetime
import shutil

auth = earthaccess.login(strategy="environment")

end_date = datetime.date.today()
start_date = end_date - datetime.timedelta(days=30)

start_date = start_date.strftime("%Y-%m-%d")
end_date = end_date.strftime("%Y-%m-%d")

results = earthaccess.search_data(
    short_name="PACE_OCI_L3M_CHL_NRT",
    temporal=(start_date, end_date),
    granule_name="*.DAY.*.0p1deg.*",
)[-7:]


hypercoast.download_nasa_data(results, "data")
files = "data/*nc"
array = hypercoast.read_pace_chla(files)
date = array.date.max().values.tolist()
mean_array = array.mean(dim="date")

filename = f"chla/chla_{date}.tif"
hypercoast.pace_chla_to_image(mean_array, filename)

shutil.copy(filename, "chla/chla_latest.tif")
print(f"Updated chla image: {filename}")

username = "opengeos"
repository = "pace-data"
tag_name = "chla"
release_id = leafmap.github_get_release_id_by_tag(username, repository, tag_name)
leafmap.github_upload_asset_to_release(username, repository, release_id, filename)
leafmap.github_upload_asset_to_release(
    username, repository, release_id, "chla/chla_latest.tif"
)
