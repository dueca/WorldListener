/* ------------------------------------------------------------------   */
/*      item            : AudioTestGui.hxx
        made by         : repa
        from template   : DuecaModuleTemplate.hxx (2022.06)
        date            : Mon Nov 28 14:26:11 2022
        category        : header file
        description     :
        changes         : Mon Nov 28 14:26:11 2022 first version
        language        : C++
        copyright       : (c)
*/

#ifndef AudioTestGui_hxx
#define AudioTestGui_hxx

// include the dusime header
#include <dueca.h>
USING_DUECA_NS;

// This includes headers for the objects that are sent over the channels
#include "comm-objects.h"

// include headers for functions/classes you need in the module
#include <gtk/gtk.h>

#if GTK_MAJOR_VERSION == 3
#include <GtkGladeWindow.hxx>
#else
#error "AudioTestGui not defined for this GTK version"
#endif
#include <dueca/AssociateObject.hxx>

/** A simulation module.

    The instructions to create an module of this class from the Scheme
    script are:

    \verbinclude port-audio-test.scm
 */
class AudioTestGui: public dueca::Module
{
  /** self-define the module type, to ease writing the parameter table */
  typedef AudioTestGui _ThisModule_;

private: // simulation data
  // declare the data you need in your simulation
  struct PATestUnit: public dueca::AssociateObject<AudioTestGui>
  {
    /** Name, identification */
    std::string          name;

    /** Interface file */
    std::string          uifile;

    /** Interface itself */
    GtkGladeWindow       window;

    /** Volume */
    float                volume;

    /** Pitch */
    float                pitch;

    /** Token to write */
    dueca::ChannelWriteToken    w_test;

    /** Token for new file, if applicable */
    boost::scoped_ptr<dueca::ChannelWriteToken> w_newfile;

    /** dueca::Callback function */
    void changeVolume(GtkRange* w, gpointer p);

    /** dueca::Callback function */
    void changePitch(GtkRange* w, gpointer p);

    /** New file selection */
    void selectFile(GtkFileChooser* w, gpointer p);

    /** Constructor with file chooser option */
    PATestUnit(const AudioTestGui *master,
               const std::string& name,
               const std::string& channel,
               const std::string& label,
               const std::string& file_channel);

    /** Constructor with only volume/pitch control. */
    PATestUnit(const AudioTestGui *master,
               const std::string& name,
               const std::string& channel,
               const std::string& label);

    /** Read and open the window */
    bool complete();
  };

  /** List of test units/windows */
  std::list<PATestUnit> testunits;

private: // channel access

private: // activity allocation
  /** You might also need a clock. Don't mis-use this, because it is
      generally better to trigger on the incoming channels */
  //PeriodicAlarm        myclock;

  /** dueca::Callback object for simulation calculation. */
  dueca::Callback<AudioTestGui>  cb1;

  /** Activity for simulation calculation. */
  dueca::ActivityCallback      do_calc;

public: // class name and trim/parameter tables
  /** Name of the module. */
  static const char* const           classname;

  /** Return the parameter table. */
  static const dueca::ParameterTable*       getMyParameterTable();

public: // construction and further specification
  /** Constructor. Is normally called from scheme/the creation script. */
  AudioTestGui(dueca::Entity* e, const char* part, const dueca::PrioritySpec& ts);

  /** Continued construction. This is called after all script
      parameters have been read and filled in, according to the
      parameter table. Your running environment, e.g. for OpenGL
      drawing, is also prepared. Any lengty initialisations (like
      reading the 4 GB of wind tables) should be done here.
      Return false if something in the parameters is wrong (by
      the way, it would help if you printed what!) May be deleted. */
  bool complete();

  /** Destructor. */
  ~AudioTestGui();

  // add here the member functions you want to be called with further
  // parameters. These are then also added in the parameter table
  // The most common one (addition of time spec) is given here.
  // Delete if not needed!

  /** Specify a time specification for the simulation activity. */
  bool setTimeSpec(const dueca::TimeSpec& ts);

  /** Request check on the timing. */
  bool checkTiming(const std::vector<int>& i);

  /** Add a control window for a */
  bool addControl(const std::vector<std::string>& args);

public: // member functions for cooperation with DUECA
  /** indicate that everything is ready. */
  bool isPrepared();

  /** start responsiveness to input data. */
  void startModule(const dueca::TimeSpec &time);

  /** stop responsiveness to input data. */
  void stopModule(const dueca::TimeSpec &time);

public: // the member functions that are called for activities
  /** the method that implements the main calculation. */
  void doCalculation(const dueca::TimeSpec& ts);
};

#endif
