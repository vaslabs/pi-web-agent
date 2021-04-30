package api

import (
	"bufio"
	"log"
	"os"
	"strings"
)

type Package_Update struct {
	Name            string
	Current_Version string
	Next_Version    string
}

func Available_Updates_From_File(location string) []Package_Update {
	_, err := os.Stat(location)
	if err != nil {
		no_packages := []Package_Update{}
		if os.IsNotExist(err) {
			log.Printf("No available updates found on %s", location)
			return no_packages
		} else {
			log.Printf("Stat error of %s: %s", location, err.Error())
			return no_packages
		}
	} else {
		packages, err := read_updates(location)
		if err != nil {
			log.Printf("Error reading available updates: %s", err)
		}
		return packages
	}
}

func Available_Updates() []Package_Update {
	return Available_Updates_From_File("/usr/lib/piwebagent2/update_check")
}

func read_updates(location string) ([]Package_Update, error) {
	file, err := os.Open(location)
	packages := []Package_Update{}

	if err != nil {
		log.Printf("Could not open %s for reading: %s", location, err.Error())
		return packages, err
	}
	defer file.Close()

	reader := bufio.NewReader(file)

	for {
		line, err := reader.ReadString('\n')
		if err != nil {
			log.Printf("Error parsing package line %s . Delete %s", line, err)
			break
		}
		package_update := parse_package(strings.Trim(line, "\n"))
		packages = append(packages, package_update)
	}

	return packages, nil
}

func parse_package(line string) Package_Update {
	package_name_starts := 0
	package_name_ends := strings.Index(line, " ")
	current_version_starts := package_name_ends + 1
	current_version_ends := strings.LastIndex(line, " ")
	next_version_starts := current_version_ends + 1
	next_version_ends := len(line)

	package_name := line[package_name_starts:package_name_ends]
	package_current_version := line[current_version_starts:current_version_ends]
	package_next_version := line[next_version_starts:next_version_ends]

	return Package_Update{package_name, package_current_version, package_next_version}
}
