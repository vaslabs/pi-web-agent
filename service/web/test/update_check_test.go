package main

import (
	"reflect"
	"testing"

	api "github.com/vaslabs/pi-web-agent/pkg"
)

func TestUpdateCheck(t *testing.T) {
	expectedPackageUpdate := api.Package_Update{Name: "package_name", Current_Version: "1.0.1", Next_Version: "1.0.2"}
	expectedPackageUpdates := []api.Package_Update{expectedPackageUpdate}
	package_updates := api.Available_Updates_From_File("test-resources/update_check")

	if !reflect.DeepEqual(expectedPackageUpdates, package_updates) {
		t.Errorf("Not equal arrays %v\n%v\n", expectedPackageUpdates, package_updates)
	}
}

