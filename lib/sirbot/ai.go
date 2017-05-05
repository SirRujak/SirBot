package sirbotlib

import (
	"encoding/json"
	"errors"
	"os"
	"path/filepath"
	"time"
)

// AI contains the main definition of the command subsystem.
type AI struct {
	moduleName              string
	boundChannel            string
	botName                 string
	commandDictFile         *os.File
	inputChannel            *chan Message
	outputChannel           *chan Message
	twitchDictFile          *os.File
	timerDictFile           *os.File
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
	commandDictionary       *CommandDict
	timerList               []*Timer
	twitchCommandDictionary *TwitchDict
	config                  *Config
	channelName             string
	paths                   pathHolder
	// This was never completed.
	spamDictionary interface{} //TODO
	// I don't know if these are needed:
	//userLevelDictionary     interface{}
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
func Startup(c *Config, ud *CommandDict) (*AI, error) {
	var a AI
	a.config = c
	a.botName = c.twAccounts.automatedAccount.name
	a.channelName = c.twChannels.defalutChannel
	a.userDict = ud.commands[a.channelName]
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
	cmdDict, err := loadCommands(a.paths.pathCommandFolders,
		a.paths.pathCommandName, a.paths.pathDefaultCommandName)
	if err != nil {
		return err
	}
	a.commandDictionary = cmdDict
	quoteDict, err := loadQuotes(a.paths.pathQuotesFolders, a.paths.pathQuotes,
		a.paths.pathDefaultQuotes)
	if err != nil {
		return err
	}
	a.quoteDict = quoteDict
	userDict, err := loadUsers(a.paths.pathUsersFolders, a.paths.pathUserName,
		a.paths.pathDefaultUsers)
	if err != nil {
		return err
	}
	a.userDict = userDict
	timerList, err := loadTimers(a.paths.pathTimerFolders,
		a.paths.pathTimerName, a.paths.pathDefaultTimerName)
	if err != nil {
		return err
	}
	a.timerList = timerList
	return nil
}

func loadFile(s1, s2 string) (*os.File, error) {
	err := os.MkdirAll(s1, 0660)
	if err != nil {
		return nil, err
	}
	tempFile, err := os.OpenFile(s2,
		os.O_RDWR|os.O_CREATE, 0660)
	if err != nil {
		return nil, err
	}
	return tempFile, nil
}

func loadString(f *os.File) ([]byte, bool, error) {
	var tempString []byte
	tempLength, err := f.Read(tempString)
	if err != nil {
		return nil, false, err
	}
	if tempLength != 0 {
		return tempString, true, nil
	}
	return tempString, false, nil
}

func loadTimers(s1, s2, s3 string) ([]*Timer, error) {
	tempTimerFile, err := loadFile(s1, s2)
	if err != nil {
		return nil, err
	}
	defer tempTimerFile.Close()
	var tempTimerList []*Timer
	tempString, length, err := loadString(tempTimerFile)
	if err != nil {
		return nil, err
	}
	if length != true {
		json.Unmarshal(tempString, &tempTimerList)
	} else {
		tempTimerFile, err := loadFile(s1, s3)
		if err != nil {
			return nil, err
		}
		defer tempTimerFile.Close()
		tempString, length, err := loadString(tempTimerFile)
		if err != nil {
			return nil, err
		}
		if length {
			json.Unmarshal(tempString, &tempTimerList)
		} else {
			return nil,
				errors.New("Unable to load default quote dict in ai.go")
		}
	}
	return tempTimerList, nil
}

func loadTwitchCommands(s1, s2, s3 string) (*TwitchDict, error) {
	tempTwitchDictFile, err := loadFile(s1, s2)
	if err != nil {
		return nil, err
	}
	defer tempTwitchDictFile.Close()
	var tempTwitchDict *TwitchDict
	var tempString []byte
	tempLength, err := tempTwitchDictFile.Read(tempString)
	if err != nil {
		return nil, err
	}
	if tempLength != 0 {
		json.Unmarshal(tempString, &tempTwitchDict)
	} else {
		tempTwitchDictFile, err := loadFile(s1, s3)
		if err != nil {
			return nil, err
		}
		defer tempTwitchDictFile.Close()
		tempString, length, err := loadString(tempTwitchDictFile)
		if err != nil {
			return nil, err
		}
		if length {
			json.Unmarshal(tempString, &tempTwitchDict)
		} else {
			return nil,
				errors.New("Unable to load default quote dict in ai.go")
		}
	}
	return tempTwitchDict, nil
}

func loadQuotes(s1, s2, s3 string) (*QuoteDict, error) {
	tempQuoteFile, err := loadFile(s1, s2)
	if err != nil {
		return nil, err
	}
	defer tempQuoteFile.Close()
	var tempQuoteDict *QuoteDict
	var tempString []byte
	tempLength, err := tempQuoteFile.Read(tempString)
	if err != nil {
		return nil, err
	}
	if tempLength != 0 {
		json.Unmarshal(tempString, &tempQuoteDict)
	} else {
		tempQuoteFile, err := loadFile(s1, s3)
		if err != nil {
			return nil, err
		}
		defer tempQuoteFile.Close()
		tempString, length, err := loadString(tempQuoteFile)
		if err != nil {
			return nil, err
		}
		if length {
			json.Unmarshal(tempString, &tempQuoteDict)
		} else {
			return nil,
				errors.New("Unable to load default quote dict in ai.go")
		}
	}
	return tempQuoteDict, nil
}

func loadUsers(s1, s2, s3 string) (*UserDictionary, error) {
	tempUserFile, err := loadFile(s1, s2)
	if err != nil {
		return nil, err
	}
	defer tempUserFile.Close()
	var tempUserDict *UserDictionary
	tempString, length, err := loadString(tempUserFile)
	if err != nil {
		return nil, err
	}
	if length != true {
		json.Unmarshal(tempString, &tempUserDict)
	} else {
		tempUserFile, err := loadFile(s1, s3)
		if err != nil {
			return nil, err
		}
		defer tempUserFile.Close()
		tempString, length, err := loadString(tempUserFile)
		if err != nil {
			return nil, err
		}
		if length {
			json.Unmarshal(tempString, &tempUserDict)
		} else {
			return nil,
				errors.New("Unable to load default quote dict in ai.go")
		}
	}
	return tempUserDict, nil
}

func loadCommands(s1, s2, s3 string) (*CommandDict, error) {
	tempDictFile, err := loadFile(s1, s2)
	if err != nil {
		return nil, err
	}
	defer tempDictFile.Close()
	var tempCommandDict *CommandDict
	var tempString []byte
	tempLength, err := tempDictFile.Read(tempString)
	if err != nil {
		return nil, err
	}
	if tempLength != 0 {
		json.Unmarshal(tempString, &tempCommandDict)
	} else {
		tempDictFile, err := loadFile(s1, s3)
		if err != nil {
			return nil, err
		}
		defer tempDictFile.Close()
		tempLength, err := tempDictFile.Read(tempString)
		if err != nil {
			return nil, err
		}
		if tempLength != 0 {
			json.Unmarshal(tempString, &tempCommandDict)
		} else {
			return nil,
				errors.New("Unable to load default command dict in ai.go")
		}
	}

	return tempCommandDict, nil
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
