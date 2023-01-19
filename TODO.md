# What needs to be done before next event

## TODO

1. Update all cars to use newest software from Donkeycars: https://github.com/autorope/donkeycar. Potentially reboot RPIs with clean OS http://docs.donkeycar.com/guide/robot_sbc/setup_raspberry_pi/ and install Dockeycar software again.
  * Check whether calibration between cars and xbox controlers work - if not working, it might be a hardware issue - test all connectors or consider getting new RPIs.
2. Update training software in Dockerized setup - currently it is at jolufan and should be moved to a Trifork repository.
  * This is to get the newest features and to ensure that the training is compatible with the data from the RPIs.
3. Create local or public available endpoint to upload training data to this endpoint.
  * This will remove the dependency of laptops from students, which could not install and run docker at the previous event.
  * Alternatively, Trifork can supply PCs with the training software installed.
