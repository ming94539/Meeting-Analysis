//
//  EmailClassificationEngine.swift
//  TestMLKit1
//
//  Created by kurtn on 7/13/17.
//  Copyright © 2017 kurtn. All rights reserved.
//

import CoreML
import Foundation

public class EmailClassificationEngine {
    var wordToIndexDict:[String:Any] = [String:Any]()
    let classificationModel: keras_model = keras_model()
    let replyThreshold = 0.5
    
    public init() {
        // ::TODO:: Improve error handling (i.e remove usage of forced unwrapping - !)
        let url = Bundle.main.url(forResource: "word2idx", withExtension: "json")
        let data = try! Data(contentsOf: url!)
        wordToIndexDict = try! JSONSerialization.jsonObject(with:data, options:[]) as! [String:Any]
    }
    
    public func emailRequiresResponse(text:String) -> (Bool, Double, [Double]) {
        var emailRequestResponse = false
        var maxSentenceConfidence = 0.0
        var confidenceIntervalPerSentence = [Double]()
        
        do {
            let sentences = splitTextIntoSentenceArray(text: text, maxArraySize:100)

            for sentence in sentences {
                
                // Convert sentence array into numeric array of length 100 (0 padded - on left)
                var sentenceData = Array<Double>(repeating:0, count:100)

                var currentIndex = 100 - sentence.count
                for word in sentence {
                    if let lookupValue = wordToIndexDict[word] as? Double {
                        sentenceData[currentIndex] = lookupValue
                    } else {
                        sentenceData[currentIndex] = 1
                    }
                    currentIndex = currentIndex + 1
                }
                
                let input = try MLMultiArray(shape:[100,1,1], dataType:.double)
                for (i,item) in sentenceData.enumerated() {
                     input[i] = NSNumber(floatLiteral: item)
                }
 
                let output = try classificationModel.prediction(input1: input, lstm_1_h_in: nil, lstm_1_c_in: nil)
                
                if let featureValue = output.featureValue(for: "output1") {
                    if let arrayValue = featureValue.multiArrayValue {
                        let confidenceInterval = arrayValue[0].doubleValue
                        if confidenceInterval >= replyThreshold {
                            emailRequestResponse = true
                        }
                        
                        if confidenceInterval >= maxSentenceConfidence {
                            maxSentenceConfidence = confidenceInterval
                        }
                        
                        confidenceIntervalPerSentence.append(confidenceInterval)
                    }
                }
            }
        } catch let error {
            print(error)
        }
        
        return (emailRequestResponse, maxSentenceConfidence,confidenceIntervalPerSentence)
    }

    func getSentenceIndexRanges(text:String, maxArraySize:Int) -> [NSRange] {
        var sentenceIndexes = [NSRange]()
        
        // Parse/Tokenize text into sentences.
        // For each sentence, parse/tokenize into words
        let tagger = NSLinguisticTagger(tagSchemes: [.lemma], options: 0)
        tagger.string = text
        let range = NSRange(location:0, length:text.utf16.count)
        let options: NSLinguisticTagger.Options = [.omitWhitespace, .omitPunctuation, .joinNames]
        
        // Tokenize into Sentences
        tagger.enumerateTags(in: range, unit: .sentence, scheme: .lemma, options: options) {
            tag, tokenRange, stop in
            sentenceIndexes.append(tokenRange)
        }
        
        return sentenceIndexes
    }

    func splitTextIntoSentenceArray(text:String, maxArraySize:Int) -> [[String]] {
        var fullText = NSString(string: text)

        // Remove \n
        fullText = fullText.replacingOccurrences(of: "\n", with: " ") as NSString

        
        // Parse/Tokenize text into sentences.
        // For each sentence, parse/tokenize into words
        let tagger = NSLinguisticTagger(tagSchemes: [.lemma], options: 0)
        tagger.string = fullText as String
        let range = NSRange(location:0, length:text.utf16.count)
        let options: NSLinguisticTagger.Options = [.omitWhitespace, .omitPunctuation, .joinNames]
        
        // Tokenize into Sentences
        var sentences:[String] = [String]()
        
        tagger.enumerateTags(in: range, unit: .sentence, scheme: .lemma, options: options) {
            tag, tokenRange, stop in
            let sentence = fullText.substring(with: tokenRange)
            sentences.append(sentence)
            
            print(sentence)
        }
        
        var sentencesWithWords:[[String]] = [[String]]()
        
        // Loop over sentence
        for sentence in sentences {
            let range = NSRange(location:0, length:sentence.utf16.count)
            tagger.string = sentence
            
            var words = [String]()
            let adjustedSentence = sentence.replacingOccurrences(of: "\n", with: " ")
            let initialWords = adjustedSentence.split(separator: " ")

            for word in initialWords {
                
                let splitAppostropheWords = word.split(separator: "’")
 
                if splitAppostropheWords.count > 1 {
                    // We have an ’ character
                    words.append(String(splitAppostropheWords[0]))
                    words.append("’")
                    words.append(String(splitAppostropheWords[1]))
                    continue;
                }
             
                let lastCharacter = word[word.index(before: word.endIndex)]
                if CharacterSet.punctuationCharacters.contains(word.unicodeScalars[word.unicodeScalars.index(before: word.unicodeScalars.endIndex)]) {
                    // last character is punctuation
                    var myWord = word
                    myWord.remove(at: myWord.index(before: myWord.endIndex))
                    words.append(String(myWord))
                    words.append(String(lastCharacter))
                } else {
                    words.append(String(word))
                }
            }
            
            sentencesWithWords.append(words)

/*
            var words = [String]()
            tagger.enumerateTags(in: range , unit: .word, scheme: .lemma, options: []) {
                tag, tokenRange, stop in
                if let wordTag = tag {

                    print(wordTag)
                    
                    // Create new empty array if our sentence is over the max size
                    if (words.count >= maxArraySize) {
                        sentencesWithWords.append(words)
                        words = [String]()
                    }
                    words.append(wordTag.rawValue)
                }
            }
            print(words)
            sentencesWithWords.append(words)
 */
/*
            var words = [String]()
            words.append("Would")
            words.append("it")
            words.append("be")
            words.append("possible")
            words.append("to")
            words.append("clarify")
            words.append("the")
            words.append("items")
            words.append("in")
            words.append("question")
            words.append("with")
            words.append("Google")
            words.append("?")
             sentencesWithWords.append(words)
*/

//            .96109
            
            /*
            var words = [String]()
            words.append("Thank")
            words.append("Kerry")
            sentencesWithWords.append(words)
*/
        }
        
        return sentencesWithWords
    }
    
}
