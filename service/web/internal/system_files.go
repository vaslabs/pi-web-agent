package shell

import (
	"strings"

	"github.com/spf13/viper"
)

func Read_Env_Config(path string, filename string) (*viper.Viper, error) {
	config := viper.New()
	config.SetConfigType("env")
	config.AddConfigPath(path)
	config.SetConfigName(filename)
	err := config.ReadInConfig()
	return config, err
}

func ReadConfigFromString(content string) (*viper.Viper, error) {
	config := viper.New()
	config.SetConfigType("env")
	err := config.ReadConfig(strings.NewReader(content))
	return config, err
}
