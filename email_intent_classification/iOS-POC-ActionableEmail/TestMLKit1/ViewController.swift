//
//  ViewController.swift
//  TestMLKit1
//
//  Created by kurtn on 7/13/17.
//  Copyright © 2017 kurtn. All rights reserved.
//

import UIKit

class ViewController: UIViewController, UITextDropDelegate  {
    
    
    @IBOutlet weak var classificationConfidence:UILabel!
   @IBOutlet weak var classificationTextView: UITextView!
   let classificationEngine = EmailClassificationEngine()
    
    func textDroppableView(_ textDroppableView: UIView & UITextDroppable, proposalForDrop drop: UITextDropRequest) -> UITextDropProposal {
        let proposal = UITextDropProposal(operation: .copy)
        proposal.dropAction = UITextDropAction.replaceAll
        return proposal
    }
    
    @IBAction func fillTextDemo1Clicked(_ sender: Any) {
        classificationTextView.attributedText = NSAttributedString(string:"How did you become so awesome?  If you could please let me know before the end of today that would be great!")
        self.view.backgroundColor = UIColor.white
        classificationConfidence.text = "???"
    }
    
    @IBAction func fillTextDemo2Clicked(_ sender: Any) {
        classificationTextView.attributedText = NSAttributedString(string:"This is just another automated email.  Nothing important to look at or see")
        self.view.backgroundColor = UIColor.white
        classificationConfidence.text = "???"
    }

    @IBAction func clearTextButtonClicked(_ sender: Any) {
        classificationTextView.attributedText = NSAttributedString(string:"")
        self.view.backgroundColor = UIColor.white
        classificationConfidence.text = "???"
    }
    
    @IBAction func classifyButtonClicked(_ sender: Any) {
      let (responseRequired,maxSentenceConfidence,confidenceIntervalPerSentence) =   classificationEngine.emailRequiresResponse(text: classificationTextView.text)
        
        if responseRequired {
            self.view.backgroundColor = UIColor.green
        } else {
            self.view.backgroundColor = UIColor.red
        }
        classificationConfidence.text = "\(maxSentenceConfidence)"

        let ranges = classificationEngine.getSentenceIndexRanges(text: classificationTextView.text, maxArraySize: 100)
        
        let classifiedString = NSMutableAttributedString(string: classificationTextView.text)
        for (index,confidenceInterval) in confidenceIntervalPerSentence.enumerated() {
            if confidenceInterval > classificationEngine.replyThreshold {
                // Highlight in green
                let range = ranges[index]
                classifiedString.addAttribute(NSAttributedStringKey.foregroundColor, value: UIColor.green, range: range)
            }
        }
        classificationTextView.attributedText = classifiedString
    }
}

