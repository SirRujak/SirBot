package sirbotlib

// Message is the data struct for passing messages
// between components.
type Message struct {
	data string
}

// Config holds all of the base configuration data for
// Sirbot.
type Config struct {
	gui         int
	twAccounts  twitchAccounts
	twChannels  twitchChannels
	twModerator twitchAutomatedModerator
	basePath    string //Where SirBot is installed.
	miscData    misc
}

type interfaceData struct {
	iconified     bool
	userList      bool
	optionsMenu   bool
	sendAs        string
	targetChannel string
	chatData      chat
}

type chat struct {
	timestamps bool
	userColors bool
	emoticons  bool
	actions    bool
	raw        bool
	channelTag bool
	textColor  bool
	silent     bool
}

type misc struct {
	twitchConnectRetries int
	other                []interface{}
}

type twitchAutomatedModerator struct {
	welcomeUsers        bool
	echo                bool
	monitorChatContent  bool
	allowCustomCommands bool
}

type twitchChannels struct {
	defalutChannel   string
	favoriteChannels []string
}

type twitchAccounts struct {
	automatedAccount account
	trustedAccount   account
}

type account struct {
	name     string
	token    string
	joinChat bool
}

// UserDict keeps a map of users and their command dictionaries.
type UserDict struct {
	users map[string]*DictNode
}

// DictNode represents one node within the command dictionary structure.
type DictNode struct {
	nodes map[string]*DictNode
}
