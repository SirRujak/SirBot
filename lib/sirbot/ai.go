package sirbotlib

import (
	"os"
	"path/filepath"
	"time"
)

// AI contains the main definition of the command subsystem.
type AI struct {
	moduleName              string
	boundChannel            string
	botName                 string
	commandDictFile         os.File
	inputChannel            *chan Message
	outputChannel           *chan Message
	twitchDictFile          os.File
	timerDictFile           os.File
	pathComName             string
	pathDefaultComName      string
	pathTimerName           string
	pathDefaultTimerName    string
	pathTwitchName          string
	tempKeyList             []interface{} //TODO
	userDict                interface{}   //TODO
	quoteDict               interface{}   //TODO
	currentTime             time.Time
	currentLine             int
	saveCommands            bool
	saveQuotes              bool
	saveUsers               bool
	lastQuoteSave           time.Time
	lastSave                time.Time
	lastUserSave            time.Time
	lastQuote               time.Time
	commandDictionary       interface{} //TODO
	timerDictionary         interface{} //TODO
	spamDictionary          interface{} //TODO
	userLevelDictionary     interface{} //TODO
	twitchCommandDictionary interface{} //TODO
	config                  *Config
	channelName             string
	paths                   pathHolder
}

type pathHolder struct {
	basePath               string
	pathCommandName        string
	pathDefaultCommandName string
	pathCommandFolders     string
	pathUserName           string
	pathDefaultUsers       string
	pathUsersFolders       string
	pathQuotes             string
	pathDefaultQuotes      string
	pathQuotesFolders      string
	pathTimerName          string
	pathDefaultTimerName   string
	pathTimerFolders       string
	pathTwitchName         string
}

// Startup is the constructor for AI. It returns a pointer to the generated
// AI system.
func Startup(c *Config, ud *UserDict) (*AI, error) {
	var a AI
	a.config = c
	a.botName = c.twAccounts.automatedAccount.name
	a.channelName = c.twChannels.defalutChannel
	a.userDict = ud.users[a.channelName]
	a.paths.basePath = c.basePath
	a.currentLine = 0
	a.lastSave = time.Now()
	a.lastQuoteSave = time.Now()
	a.lastUserSave = time.Now()
	a.lastQuote = time.Now().Add(time.Duration(5) * time.Second)
	a.getCurrentTime()
	a.paths.makeDictPathName(a.channelName)
	err := a.loadData()
	if err != nil {
		return nil, err
	}
	return &a, nil
}

func (a *AI) getCurrentTime() {
	a.currentTime = time.Now()
}

func (a *AI) loadData() error {
	err := os.MkdirAll(a.paths.pathCommandFolders, 0655)
	if err != nil {
		return err
	}

	return nil
}

func (p *pathHolder) makeDictPathName(channelName string) {
	p.pathCommandName = filepath.Join(p.basePath, "/data/sirbot/commands/",
		channelName, "/commands.json")
	p.pathDefaultCommandName = filepath.Join(p.basePath,
		"/data/sirbot/commands/defaultCommands/commands.json")
	p.pathCommandFolders = filepath.Join(p.basePath, "/data/sirbot/commands/",
		channelName)
	p.pathUserName = filepath.Join(p.basePath, "/data/sirbot/users/",
		channelName, "/users.json")
	p.pathDefaultUsers = filepath.Join(p.basePath,
		"/data/sirbot/users/defaultUsers/users.json")
	p.pathUsersFolders = filepath.Join(p.basePath, "/data/sirbot/users/",
		channelName)
	p.pathQuotes = filepath.Join(p.basePath, "/data/sirbot/quotes/",
		channelName, "/quotes.json")
	p.pathDefaultQuotes = filepath.Join(p.basePath,
		"/data/sirbot/quotes/defaultQuotes/quotes.json")
	p.pathQuotesFolders = filepath.Join(p.basePath, "/data/sirbot/quotes/",
		channelName)
	p.pathTimerName = filepath.Join(p.basePath, "/data/sirbot/timers/",
		channelName, "/timers.json")
	p.pathDefaultTimerName = filepath.Join(p.basePath,
		"/data/sirbot/timers/defaultTimers/timers.json")
	p.pathTimerFolders = filepath.Join(p.basePath, "/data/sirbot/timers/",
		channelName)
	p.pathTwitchName = filepath.Join(p.basePath,
		"/data/sirbot/twitchcommands/twitchcommands.json")
}
