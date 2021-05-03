package shell

import (
	"os"
	"path"
	"sync"
)

const (
	PWA_ROOT_PATH_PREFIX = "PWA_ROOT_PATH_PREFIX"
)

func get_env(key string, fallback string) string {
	value := os.Getenv(key)
	if len(value) == 0 {
		return fallback
	}
	return value
}

type PathResolver struct {
	root_prefix string
}

func (resolver *PathResolver) Resolve_Path(path_to_resolve string) string {
	return path.Join(resolver.root_prefix, path_to_resolve)
}

var pwa_resolver *PathResolver
var create_pwa_resolver_once sync.Once

func get_PWA_Root_Path_Prefix() string {
	return get_env(PWA_ROOT_PATH_PREFIX, string('/'))
}
func GetPwaPathResolver() *PathResolver {
	create_pwa_resolver_once.Do(func() {
		var root_prefix string = get_PWA_Root_Path_Prefix()
		pwa_resolver = &PathResolver{root_prefix: root_prefix}
	})
	return pwa_resolver
}
