package sirbotlib

import "time"

// Message is the data struct for passing messages
// between components.
type Message struct {
	userName        string
	channelName     string
	timeStamp       *time.Time
	messageContents string
	isLocal         bool
	chatType        int
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

// CommandDict keeps a map of users and their command dictionaries.
type CommandDict struct {
	commands       map[string]*CommandNode
	levels         []string
	outlinks       []string
	linkDict       map[string]map[string][]string
	responseDict   map[string]*responseLevel
	conditions     map[string]string
	links          map[string]*linkHolder
	levelStructure map[interface{}]interface{} //TODO
}

// CommandNode represents one node within the command dictionary structure.
type CommandNode struct {
	nodes     map[string]*CommandNode
	link      string
	limits    map[string]*limitContainer
	active    bool
	isGlobal  bool
	isCommand bool
}

type linkHolder struct {
	singleLink map[string]*linkData
}

type linkData struct {
	lastEditor string
	creator    string
	linkType   string
	timeLimit  int
	lineLimit  int
	response   string
	groups     map[string]bool
	users      map[string]bool
}

type responseLevel struct {
	responseIn  []string
	responseOut []string
}

type limitContainer struct {
	lastTime time.Time
	lastLine int
	total    int
}

// UserDictionary keeps data about all of the known users in chat.
type UserDictionary struct {
	users []user
}

type user struct {
	groups []string
	level  string
}

// QuoteDict holds a list of quotes and a map of the same quotes.
type QuoteDict struct {
	quoteList []*quote
	quotes    map[string]bool
}

type quote struct {
	quoteData    string
	quoteCreator string
}

// TwitchDict contains a map of users commands to twitch specific commands.
type TwitchDict struct {
	twitchCommands map[string]string
}

// Timer holds the specifications for a single timer element.
type Timer struct {
	totalTime time.Duration
	hours     time.Duration
	minutes   time.Duration
	seconds   time.Duration
	active    bool
	command   string
}
