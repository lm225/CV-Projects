import java.io.*;


public class Eliza {

	//method called in the main method, used to prioritize default 
	public void start() throws IOException{

		Eliza e = new Eliza();
		Default de = new Default();

		if (e.readConsole() == false){
			de.defaultResponses();

		} 
	}

	//prints out the starting sentence
	public void welcomeMessage() throws IOException{

		try{
			String welcome;
			BufferedReader reader = new BufferedReader(new FileReader ("script.txt"));
			welcome = reader.readLine();
			System.out.println(welcome);
		}
		catch(FileNotFoundException e){
			System.out.println("The File Specified Could Not Be Found");
		}


	}


	//method to prioritize and call the decomposition and reassembly methods
	public boolean readConsole() throws IOException{

		BufferedReader consoleReader = new BufferedReader(new InputStreamReader(System.in));

		PreSubRules presub = new PreSubRules();
		Keywords keywords = new Keywords();
		People people = new People();
		Quit quit = new Quit();
		Reconstruct re = new Reconstruct();
		Eliza el = new Eliza();

		boolean exit = false;
		boolean output = true;
		try {
			//keep reading console and calling methods until a quit command is input (exit == true)
			while(exit == false){
				String read = consoleReader.readLine();
				String [] words = read.split(" ");



				output = true;


				//prioritization of methods
				if ((presub.preSubRule(el.convert(words))) == false){
					if ((keywords.findKeywords(el.convert(words))) == false){
						if ((people.findPeople(el.convert(words))) == false){
							if(re.reconstructSentence(el.convert(words)) == false){
								if (quit.endProgram(el.convert(words)) == false){
									output = false;
									return output;
								} else exit = true; 


							}

						}
					}
				}

			}


		} catch (IOException e) {
			System.out.println("IO Exception");

		}		
		return output;
	}

	//method to convert the users input into lower case 
	public String[] convert(String[] words){

		for(int i = 0; i < words.length; i ++){
			words[i] = words[i].toLowerCase();

		}

		return words;

	}


}




