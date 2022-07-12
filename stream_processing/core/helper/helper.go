package helper

import "strings"

func JoinStringsByVerticalBar(elements ...string) string {
	return strings.Join(elements, "|")
}
