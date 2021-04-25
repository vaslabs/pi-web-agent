package shell

import (
	"fmt"
	"os"
	"path"

	"github.com/spf13/viper"
)

type RPI_Config interface {
	Port() uint32
	Password_Hash() string
	TLS_Cert_File() string
	TLS_Key_File() string
	TLS_Port() uint32
	Update_Passphrase(phrase string)
}

type Dynamic_RPI_Config struct {
	config *viper.Viper
}

const (
	PASSWORD_HASH_KEY   = "PASSWORD_HASH"
	PORT_NUMBER_KEY     = "PORT_NUMBER"
	TLS_CERT_FILE_KEY   = "TLS_CERT_FILE"
	TLS_KEY_FILE_KEY    = "TLS_KEY_FILE"
	TLS_PORT_NUMBER_KEY = "TLS_PORT_NUMBER"
)

func (config *Dynamic_RPI_Config) Password_Hash() string {
	return config.config.GetString(PASSWORD_HASH_KEY)
}

func (config *Dynamic_RPI_Config) Port() uint32 {
	return config.config.GetUint32(PORT_NUMBER_KEY)
}

func (config *Dynamic_RPI_Config) TLS_Cert_File() string {
	return config.config.GetString(TLS_CERT_FILE_KEY)
}

func (config *Dynamic_RPI_Config) TLS_Key_File() string {
	return config.config.GetString(TLS_KEY_FILE_KEY)
}

func (config *Dynamic_RPI_Config) TLS_Port() uint32 {
	return config.config.GetUint32(TLS_PORT_NUMBER_KEY)
}

func (config *Dynamic_RPI_Config) Update_Passphrase(phrase string) {
	config.config.Set(PASSWORD_HASH_KEY, phrase)
	config.config.WriteConfig()
}

func Load_PWA_config(path string) RPI_Config {
	viper_config, _ := load_PWA_config(path)
	return &Dynamic_RPI_Config{viper_config}

}

func Load_RPI_PWA_Config() RPI_Config {
	pwa_path := "/etc/piwebagent2"
	config_path := "config"
	if _, err := os.Stat(pwa_path); err == nil {
		return Load_PWA_config(path.Join(pwa_path, config_path))
	}
	return Load_PWA_config(config_path)
}

func load_PWA_config(path string) (*viper.Viper, error) {
	config := viper.New()
	config.SetDefault(PASSWORD_HASH_KEY, "")
	config.SetDefault(PORT_NUMBER_KEY, uint32(8080))
	config.SetDefault(TLS_PORT_NUMBER_KEY, uint32(8443))
	config.SetDefault(TLS_CERT_FILE_KEY, "/etc/pwa_ca/rpi/cert.pem")
	config.SetDefault(TLS_KEY_FILE_KEY, "/etc/pwa_ca/rpi/key.pem")
	config.AddConfigPath(path)
	config.SetConfigType("env")
	config.WatchConfig()
	config.ReadInConfig()
	err := config.SafeWriteConfig()
	if err != nil {
		fmt.Printf("Error writing config for the first time %s\n", err.Error())
	}
	return config, err

}
